from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as logout_user

from .common import get_base_context
from .forms import EnterForm


# Create your views here.
def index(request: HttpRequest):
    return redirect("tasks")


def tasks(request: HttpRequest):
    if request.user.is_authenticated:
        context = get_base_context(request)
        return render(request, "main/index.html", context)
    else:
        return redirect("enter")


def leaderboard(request: HttpRequest):
    context = get_base_context(request, False)
    return render(request, "main/leaderboard.html", context)


def enter(request: HttpRequest):
    if request.method == "POST":
        form = EnterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create_user(form.cleaned_data["username"])
                user.save()

            if user.has_usable_password():
                return HttpResponseForbidden()

            login(request, user)

            return HttpResponseRedirect("/")
    else:
        form = EnterForm()

    return render(request, "main/enter.html", {"form": form})


def logout(request: HttpRequest):
    logout_user(request)
    return HttpResponseRedirect("/enter")
