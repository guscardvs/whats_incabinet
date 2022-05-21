from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest

from core import utils
from profiles import services
# Create your views here.


class Register(View):

    template_name = 'register.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name)

    def post(self, request: HttpRequest):
        form = utils.pop_csrf(request.POST, 'password2')
        user = services.create_user_profile(services.CreateUserPayload(**form))
        login(request, user)
        return redirect('home')



class Access(View):

    template_name = 'access.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name)

    def post(self, request: HttpRequest):
        form = utils.pop_csrf(request.POST)
        user = authenticate(request, **form)
        if user is None:
            return render(request, self.template_name, {
                'error': 'Ops, algum erro ocorreu :(, Tente novamente.'
            })
        login(request, user)
        return redirect('home')

    
@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('access')