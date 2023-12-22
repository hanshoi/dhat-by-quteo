from django.shortcuts import render, get_object_or_404


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

