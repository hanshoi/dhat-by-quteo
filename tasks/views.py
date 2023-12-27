from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from qframe.shortcuts import render_htmx

# Create your views here.


@login_required
def index(request):
    return render_htmx(request, "index.html")
