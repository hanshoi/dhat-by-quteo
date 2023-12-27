from django import forms
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from qframe.shortcuts import render_htmx
from tasks.models import Task


@login_required
def task_list(request):
    tasks = Task.objects.prefetch_related("tags").order_by("-created_at").all()[:30]
    return render_htmx(request, "task_list.html", {"tasks": tasks})


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["created_at"]


@login_required
def add_task(request):
    return render(request, "task.html", {"form": AddTaskForm()})
