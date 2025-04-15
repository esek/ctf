from django.http import HttpRequest, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as logout_user

from ctef_core.common import get_base_context, get_default_competition
from ctef_core.decorators import TaskDesc
from ctef_core.models import Task, TaskAttempt, TaskClue, CompetitionParticipation

from .forms import EnterForm


# Create your views here.
def index(request: HttpRequest):
    return redirect("tasks")


def tasks(request: HttpRequest):
    if request.user.is_authenticated:
        context = get_base_context(request)
        return render(request, "ctef_web/index.html", context)
    else:
        return redirect("enter")


def leaderboard(request: HttpRequest):
    context = get_base_context(request, False)

    default_competition = get_default_competition()
    participants = CompetitionParticipation.objects.filter(
        competition=default_competition
    ).order_by("score")

    context["participants"] = participants

    return render(request, "ctef_web/leaderboard.html", context)


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

    return render(request, "ctef_web/enter.html", {"form": form})


def logout(request: HttpRequest):
    logout_user(request)
    return HttpResponseRedirect("/enter")


def config_hints_view(task_desc: TaskDesc):
    def hints(request: HttpRequest):
        task = Task.objects.get(slug=task_desc.slug)

        context = get_base_context(request, True)
        context["task"] = task

        task_clue_count = TaskClue.objects.filter(task=task).count()

        try:
            attempt = TaskAttempt.objects.get(task=task, user=request.user)
        except TaskAttempt.DoesNotExist:
            attempt = None

        if request.method == "POST":
            if attempt.clue_count < task_clue_count:
                attempt.clue_count = attempt.clue_count + 1
                attempt.save()

        if attempt is not None:
            clues = TaskClue.objects.filter(task=task).order_by("index")[
                : attempt.clue_count
            ]

            context["clues"] = [clue.clue for clue in clues]
            context["clues_available"] = attempt.clue_count < task_clue_count

        return render(request, "ctef_web/clues.html", context)

    return hints
