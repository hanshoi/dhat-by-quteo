from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, "index.html")


@login_required
def content(request):
    return HttpResponse(
        format_html(
            """
<div class="overflow-hidden rounded-lg bg-gray-200">
  <div class="px-4 py-5 sm:p-6">
    <!-- Content goes here -->
  </div>
</div>
    """
        )
    )


def _create_navigation(
    name: str,
    icon: str,
    url_name: str,
    children: list[dict] | None = None,
    active: bool = False,
) -> dict:
    return {
        "name": name,
        "active": active,
        "icon": f"icons/{icon}.svg",
        "url": reverse(url_name),
        "sidebar_item": reverse("sidebar-item", args=[name.lower()]),
        "children": children or [],
    }


@login_required
def sidebar(request, item=None):
    navigations = {
        "dashboard": _create_navigation("Dashboard", "house", "index", active=True),
        "team": _create_navigation(
            "Team",
            "people",
            "team",
            [{"name": "Prospects", "url": reverse("dummy")}],
        ),
        "projects": _create_navigation("Projects", "folder", "dummy"),
        "calendar": _create_navigation("Calendar", "calendar", "dummy"),
        "documents": _create_navigation("Documents", "documents", "dummy"),
        "reports": _create_navigation("Reports", "pie", "dummy"),
    }
    if item:
        deactivation = request.GET.get("deactivate", "").lower() == "true"
        nav = navigations[item]
        nav["active"] = False if deactivation else True
        response = render(request, "sidebar.html#navitem", {"nav": nav, "key": item})
        if not deactivation:
            response.headers["HX-Trigger"] = "nav-link-deactivate"
        return response
    else:
        return render(request, "sidebar.html", {"navigations": navigations})
