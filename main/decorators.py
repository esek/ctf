import functools
from django.utils.text import slugify

from .common import task_view_wrapper, get_module_key


class TaskDesc:
    """Defines a task registered within the system"""

    def __init__(
        self,
        name: str,
        slug: str,
        wrapped_view,
        module: str,
        desc: None | str = None,
        clues: None | str = None,
    ) -> None:
        self.name = name
        self.slug = slug
        self.view = wrapped_view
        self.module = module
        self.desc = desc
        self.clues = clues

    def top_level_module(self):
        return get_module_key(self.module)


MODULE_TASKS: dict[str, TaskDesc] = {}


def define_task(name, desc: None | str = None, clues: None | str = None):
    """Defines a new task associated to the decorated view."""

    def decorator(view):
        functools.wraps(view)

        slug = slugify(name)
        wrapped_view = task_view_wrapper(view, slug)

        task = TaskDesc(name, slug, wrapped_view, view.__module__, desc, clues)

        key = task.top_level_module()

        if key not in MODULE_TASKS:
            MODULE_TASKS[key] = [task]
        else:
            MODULE_TASKS[key].append(task)

        return wrapped_view

    return decorator
