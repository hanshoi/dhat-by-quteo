from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django.template import Context, Template

from accounts.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model= User
        fields = ['username', 'password1', 'password2']


def view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You are now able to log in"
            )
            return redirect("login")
    else:
        form = UserRegisterForm()
        return render(request, "register.html", {"form": form})