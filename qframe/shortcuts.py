from django.http import HttpResponse
from django.shortcuts import render


def render_htmx(
    request, template: str, context: dict | None = None, base: str | None = None
) -> HttpResponse:
    context = context or {}
    if request.htmx:
        context["base"] = "partial.html"
        return render(request, f"{template}", context or {})
    else:
        context["base"] = base or "index.html"
        return render(request, template, context or {})
