import os
from typing import Any
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.db.utils import IntegrityError

from main.models import TaskModule, Task
from main.decorators import MODULE_TASKS, TaskDesc
from main.common import fetch_ctf_modules, get_module_key


def read_markdown_file(task: TaskDesc) -> str:
    with open(f"{task.top_level_module()}/{task.desc}") as f:
        return f.read()


class Command(BaseCommand):
    help = "Register all modules within the database"

    def handle(self, *args: Any, **options: Any) -> str | None:
        mods = fetch_ctf_modules()

        for mod in mods:
            module = TaskModule()
            module.name = mod.name
            module.title = mod.display_name

            try:
                module.save()
            except IntegrityError:
                print(
                    f'Module "{mod.display_name}" has already been added, skipping...'
                )
                continue

            key = get_module_key(mod.__module__)
            module_tasks = MODULE_TASKS.get(key)

            if module_tasks is None:
                continue

            for task_desc in module_tasks:
                name = task_desc.name

                task = Task()
                task.name = name
                task.slug = task_desc.slug
                task.module = module
                task.points = 10

                if task_desc.desc is not None:
                    task.desc = read_markdown_file(task_desc)

                try:
                    task.url = reverse(name)
                except NoReverseMatch:
                    print("[ERROR] Mismatch between task view name and function name!")
                    continue

                task.save()
