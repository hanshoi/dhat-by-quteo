from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(default="", blank=True, null=False)
    assignee = models.ForeignKey(
        get_user_model(), default=None, null=True, blank=True, on_delete=models.SET_NULL
    )
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self) -> str:
        return self.title
