from django.http import HttpResponse
from django.shortcuts import render


def render_htmx(request, template: str, context: dict | None = None) -> HttpResponse:
    if request.htmx:
        return render(request, f"{template}#main", context or {})
    else:
        return render(request, template, context or {})
