
import dataclasses
from typing import Optional, Self
from django.forms import Form

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

@dataclasses.dataclass
class ViewContext:
    template: str
    request: HttpRequest
    form: Optional[Form] = None


class View:
    def __init__(self, template: Optional[str] = None, form_class: Optional[type[Form]] = None):
        self.form_success_handler = None
        self.get_handler = None
        self.template = template
        self.form_class = form_class

    def post(self, form_class: Optional[type[Form]] = None):
        self.form_class = form_class
        def inner(func):
            self.form_success_handler = func
        return inner

    def get(self, template: Optional[str]):
        if template:
            self.template = template
        if self.template is None:
            raise AttributeError("Template not defined!")
        def inner(func):
            self.get_handler = func
        return inner

    def to_view(self):
        def _view(request: HttpRequest) -> HttpResponse:
            assert self.template, "No template defined"
            if request.method == "POST":
                if self.form_class is not None:
                    form = self.form_class(request.POST)
                    if form.is_valid():
                        form.save()
                        if self.form_success_handler:
                            return self.form_success_handler(ViewContext(self.template, request, form))
                        else:
                            return render(request, self.template, self.get_handler(request) if self.get_handler else {})
                else:
                    raise Http404("Form has not been defined for this view")
            elif request.method == "GET" and self.template:
                context = self.get_handler(request) if self.get_handler else {}
                if self.form_class:
                    context["form"] = self.form_class()
                return render(request, self.template, context)
            raise Http404(f"No handler for method {request.method} implemented")
        return _view

