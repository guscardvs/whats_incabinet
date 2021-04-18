from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from base.exception import ViewException
from base.view import PydanticView, RequestWrapper, decoratedview
from users.models import Profile, User
from users.dtos import InvalidPassword, LoginDTO, RegisterDTO
from django.contrib.auth import authenticate, login

# Create your views here.
class Register(PydanticView):

    template_name = "register.html"

    @decoratedview()
    def get(self):
        return

    @decoratedview()
    def post(self, wrapper: RequestWrapper[RegisterDTO]):
        profile = Profile.objects.create(wrapper.form())
        if profile:
            login(wrapper.request, profile.user)
            return "home"
        else:
            raise ViewException(message="Nome de usuário já existe")

    @decoratedview()
    def error(self, errors: list[InvalidPassword]):
        return {"error": "\n".join(item.message for item in errors)}


class Access(PydanticView):
    template_name = "access.html"

    @decoratedview()
    def get(self):
        return

    @decoratedview()
    def post(self, wrapper: RequestWrapper[LoginDTO]):
        user = self.authenticate(wrapper)
        login(wrapper.request, user)
        return "home"

    def authenticate(self, wrapper: RequestWrapper[LoginDTO]):
        form = wrapper.form()
        if User.objects.filter(username=form.username).exists():
            user = authenticate(wrapper.request, **form.dict())
            if user is None:
                raise ViewException("Senha incorreta")
            return user
        else:
            raise ViewException("Nenhum usuário com esse nome encontrado")

    @decoratedview()
    def error(self, errors: list[ViewException]):
        return {"error": "\n".join(item.message for item in errors)}
