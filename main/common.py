from django.apps import apps
from django.http import HttpRequest, HttpResponseBadRequest
from django.contrib.auth.models import User

from main.models import Task, TaskAttempt
from main.forms import SecretForm


def get_module_key(module):
    return module.split(".")[0]


def fetch_ctf_modules(additional_flag=None):
    """Fetches all django apps with modules installed within them."""

    def check(config):
        try:
            return config.has_tasks and (
                True if additional_flag is None else config.additional_flag
            )
        except AttributeError:
            return False

    mods = [c for c in apps.get_app_configs() if check(c)]
    return mods


def get_base_context(request, include_tasks=True):
    user = request.user
    context = {"user": request.user}

    if include_tasks:
        tasks = Task.objects.all()
        attempts = TaskAttempt.objects.filter(user=user)

        passed_tasks = [a.task.id for a in attempts if a.passed]
        module_tasks = dict(
            map(lambda t: (t.module, [(t, t.id in passed_tasks)]), tasks)
        )

        context["module_tasks"] = module_tasks

    return context


def validate_secret(attempt: TaskAttempt, secret: str) -> bool:
    if attempt.task.secret == secret:
        attempt.passed = True
        attempt.save()

        return True
    else:
        return False


def task_view_wrapper(view, slug):
    def wrapper(request: HttpRequest):
        context = get_base_context(request)

        user = request.user

        task = Task.objects.get(slug=slug)
        context["task"] = task

        attempt, _ = TaskAttempt.objects.get_or_create(
            task=task, user=user, defaults={"points": task.points}
        )
        context["task_attempt"] = attempt

        if request.method == "POST":
            secret_form = SecretForm(request.POST)

            if secret_form.is_valid():
                secret = secret_form.cleaned_data["secret"]

                if validate_secret(attempt, secret):
                    context["passed"] = True
            else:
                return HttpResponseBadRequest("Secret data was incorrectly submitted.")
        else:
            secret_form = SecretForm()

        context["secret_form"] = secret_form

        return view(request, context)

    return wrapper
