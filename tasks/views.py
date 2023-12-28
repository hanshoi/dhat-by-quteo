from django import forms
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from qframe.constants import Swap
from qframe.response import HtmxResponse
from qframe.shortcuts import render_htmx, render_with_base
from tasks.models import Task


@login_required
def task_list(request):
    tasks = Task.objects.prefetch_related("tags").order_by("-created_at").all()[:30]
    return render_with_base(request, "task_list.html", {"tasks": tasks})


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
            return (
                render_htmx(request, "task_list.html#task", {"task": task})
                .trigger("refresh-slideover")
                .reswap(Swap.AFTERBEGIN)
                .retarget("#task-list")
            )
    return render(request, "add_task.html", {"form": TaskForm()})


@login_required
def edit_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            return (
                render_htmx(request, "task_list.html#task", {"task": task})
                .trigger("close-slideover")
                .reswap(Swap.OUTER)
                .retarget(f"#tasklist-item-{task.id}")
            )
    return render(
        request, "edit_task.html", {"form": TaskForm(instance=task), "task": task}
    )


@login_required
@require_http_methods(["DELETE"])
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return (
        HtmxResponse("")
        .trigger("close-slideover")
        .reswap(Swap.OUTER)
        .retarget(f"#tasklist-item-{task_id}")
    )
