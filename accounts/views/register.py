from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from accounts.models import User
from django.contrib.auth.forms import UserCreationForm

from ...qframe.views import View, ViewContext


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


view = View(template="register.html")


@view.post(form_class=UserRegisterForm)
def _form_success(ctx: ViewContext) -> HttpResponse:
    username = ctx.form.cleaned_data.get("username")
    messages.success(
        ctx.request, f"Your account has been created! You are now able to log in"
    )
    return redirect("login")
