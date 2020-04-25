from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from core import models
# Create your views here.
class Register(View):
    template_name = 'register.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = {key:value for key, value in request.POST.items() if key not in ['password2', 'csrfmiddlewaretoken']}
        user = User.objects.create_user(**form)
        profile = models.Profile(user=user).save()
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name, {
                'error':'Ops, algum erro ocorreu :(, Tente novamente.'
            })
            
class Access(View):
    template_name = 'access.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = {key:value for key,value in request.POST.items() if key not in ['csrfmiddlewaretoken']}
        user = authenticate(request, **form)
        if user is not None:
            return redirect('home')
        else:
            return render(request, self.template_name, {
                'error':'Ops, algum erro ocorreu :(, Tente novamente.'
            })
            
            
@login_required
def home(request):
    return render(request, 'home.html')


class ListItems(View, LoginRequiredMixin):
    
    template_name = 'list-items.html'
    
    @property
    def context(self, request: HttpRequest) -> dict:
        return dict(items=models.Profile.objects.get(user=request.user).items)
    
    def get(self, request):
        return render(request, self.template_name, self.context)
    
    def post(self, request):
        form = {key:value for key, value in request.POST.items() if key not in ['csrfmiddlewaretoken']}        
        context = dict(items=models.Profile.objects.get(user=request.user).items)
        profile = models.Profile.get(user=request.user)
        try:
            check = models.Item.objects.get(name=form['name'])
            profile.item.add(check)
        except models.Item.DoesNotExist:
            item = models.Item(**form)
            if item is not None:
                item.save()
                profile.item.add(item)
            else:
                context = self.context
                context['error'] = 'Ops, algum erro ocorreu :(, Tente novamente.'
                return render(request, self.template_name, context)
        finally:
            return render(request, self.template_name, self.context)
        
        
def logout_view(request):
    logout(request)
    return redirect('access')