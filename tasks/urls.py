from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="tasks"),
    path("add/", views.add_task, name="add")
]
