from typing import Any
from django.template import loader

from qframe.response import HtmxResponse


def render_htmx(
    request,
    template: str,
    context: dict[str, Any] | None = None,
    content_type: str | None = None,
    status: int | None = None,
    using: str | None = None,
) -> HtmxResponse:
    content = loader.render_to_string(template, context or {}, request, using=using)
    return HtmxResponse(content, content_type, status)


def render_with_base(
    request, template: str, context: dict | None = None, base: str | None = None
) -> HtmxResponse:
    context = context or {}
    if request.htmx:
        context["base"] = "partial.html"
        return render_htmx(request, f"{template}", context or {})
    else:
        context["base"] = base or "index.html"
        return render_htmx(request, template, context or {})
