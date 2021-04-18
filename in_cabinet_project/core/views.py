from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def home(request):
    return render(request, "home.html")


def logout_view(request):
    logout(request)
    return redirect("access")
