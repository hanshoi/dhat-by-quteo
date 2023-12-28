from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from qframe.shortcuts import render_htmx
from tasks.models import Task


@login_required
def task_list(request):
    tasks = Task.objects.prefetch_related("tags").order_by("-created_at").all()[:30]
    return render_htmx(request, "task_list.html", {"tasks": tasks})


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ["created_at"]


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            response = render(request, "task_list.html#task", {"task": task})
            response.headers["HX-Trigger"] = "refresh-slideover"
            response.headers["HX-Reswap"] = "afterbegin"
            response.headers["HX-Retarget"] = "#task-list"
            return response
    return render(request, "add_task.html", {"form": TaskForm()})


@login_required
def edit_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            response = render(request, "task_list.html#task", {"task": task})
            response.headers["HX-Trigger"] = "close-slideover"
            response.headers["HX-Reswap"] = "outerHTML"
            response.headers["HX-Retarget"] = f"#tasklist-item-{task.id}"
            return response
    return render(
        request, "edit_task.html", {"form": TaskForm(instance=task), "task": task}
    )
