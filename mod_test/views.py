from django.shortcuts import render
from django.http import HttpRequest

from main.decorators import define_task

from main.models import Task


# Create your views here.
@define_task(name="Test Task", desc="test_task.md", clues="test_task_clues.md")
def test_task(request: HttpRequest, context):
    return render(request, "mod_test/index.html", context)
