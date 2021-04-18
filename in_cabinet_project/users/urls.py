from django.urls import path
from users import views


urlpatterns = [
    path("register/", views.Register.as_view(), name="register"),
    path("login/", views.Access.as_view(), name="access"),
]
