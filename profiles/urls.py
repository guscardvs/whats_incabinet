from django.urls import path

from profiles import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.Register.as_view(), name='register'),
    path('access', views.Access.as_view(), name='access'),
    path('logout', views.logout_view, name='logout'),
]
