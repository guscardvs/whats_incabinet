from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from core import models, utils


class Register(View):

    template_name = 'register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = utils.format_form(request.POST, 'password2')
        user = User.objects.create_user(**form)
        profile = models.Profile(user=user).save()
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name, {
                'error': 'Ops, algum erro ocorreu :(, Tente novamente.'
            })


class Access(View):

    template_name = 'access.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = utils.format_form(request.POST)
        user = authenticate(request, **form)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, self.template_name, {
                'error': 'Ops, algum erro ocorreu :(, Tente novamente.'
            })


@login_required
def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('access')
