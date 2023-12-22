from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm


def render_htmx(request, template, context=None, **kwargs):
    if request.htmx:
        base = "partial.html"
    else:
        base = "base.html"
    if context:
        context["base"] = base
    else:
        context = {"base": base}
    return render(request, template, context, **kwargs)

def index(request):
    return render_htmx(request, "index.html")

def about(request):
    return render_htmx(request, "about.html")


def register(request):
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
        return render_htmx(request, "register.html", {"form": form})