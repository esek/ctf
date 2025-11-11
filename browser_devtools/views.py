from django.http import HttpRequest
from django.shortcuts import render
from ctef_core.decorators import define_task


# Create your views here.
@define_task(name="Watch your head!", clues="clues/watch_your_head.md")
def watch_your_head(request: HttpRequest, context):
    return render(request, "browser_devtools/watch_your_head.html", context)

@define_task(name="Courier intercept")
def courier_intercept(request: HttpRequest, context):
    return render(request, "browser_devtools/courier_intercept.html", context)