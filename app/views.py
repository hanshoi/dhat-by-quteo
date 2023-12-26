from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def render_htmx(request, template: str, context: dict | None = None) -> HttpResponse:
    if request.htmx:
        return render(request, f"{template}#main", context or {})
    else:
        return render(request, template, context or {})


@login_required
def index(request):
    return render_htmx(request, "index.html")


@login_required
def content(request):
    return render_htmx(request, "index.html")


def _create_navigation(
    name: str,
    icon: str,
    url_name: str,
    children: list[dict] | None = None,
) -> tuple[str, dict]:
    key = name.lower()
    return (
        key,
        {
            "name": name,
            "active": False,
            "icon": f"icons/{icon}.svg",
            "url": reverse(url_name),
            "sidebar_item": reverse("sidebar-item", args=[key]),
            "children": children or [],
        },
    )


@login_required
def sidebar(request, item=None):
    navigations = dict(
        [
            _create_navigation("Dashboard", "house", "index"),
            _create_navigation(
                "Team",
                "people",
                "team",
                [{"name": "Prospects", "url": reverse("dummy")}],
            ),
            _create_navigation("Projects", "folder", "dummy"),
            _create_navigation("Calendar", "calendar", "dummy"),
            _create_navigation("Documents", "documents", "dummy"),
            _create_navigation("Reports", "pie", "dummy"),
        ]
    )
    if item:
        deactivation = request.GET.get("deactivate", "").lower() == "true"
        nav = navigations[item]
        nav["active"] = False if deactivation else True
        response = render(request, "sidebar.html#navitem", {"nav": nav, "key": item})
        if not deactivation:
            response.headers["HX-Trigger"] = "nav-link-deactivate"
        return response
    else:
        key = _path_to_key(request.GET.get("url", "/"), navigations)
        if key:
            navigations[key]["active"] = True
        return render(request, "sidebar.html", {"navigations": navigations})


def _path_to_key(path: str, navigations: dict) -> str | None:
    if path == "/":
        return "dashboard"

    for key, nav in navigations.items():
        if path[:6] == nav["url"][:6]:
            return key
