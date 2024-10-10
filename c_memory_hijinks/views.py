from django.shortcuts import render
from django.http import HttpRequest

from main.decorators import define_task

from main.models import Task


# Create your views here.
@define_task(
    name="Secret passcode", desc="secret_passcode.md", clues="secret_passcode_clues.md"
)
def secret_passcode(request: HttpRequest, context):
    return render(request, "c_memory_hijinks/index.html", context)
