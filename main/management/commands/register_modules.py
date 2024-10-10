import re
from typing import Any, Generator
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.db.utils import IntegrityError

from main.models import TaskModule, Task, TaskClue
from main.decorators import MODULE_TASKS, TaskDesc
from main.common import fetch_ctf_modules, get_module_key


def read_file_contents(path: str) -> str:
    with open(path) as f:
        return f.read()


def read_desc_markdown(desc: TaskDesc) -> str:
    return read_file_contents(f"{desc.top_level_module()}/{desc.desc}")


def find_hints_delimiters(markdown: str):
    return [m.start() for m in re.finditer("# ", markdown)]


def read_hints_markdown(desc: TaskDesc) -> Generator[str, None, None]:
    """Reads hint from markdown file by top level header (#)."""
    contents = read_file_contents(f"{desc.top_level_module()}/{desc.clues}")
    delimiters = find_hints_delimiters(contents)

    delimiters.append(len(contents) - 1)

    last = delimiters.pop(0)

    while len(delimiters) > 0:
        next = delimiters.pop(0)

        hint = contents[last:next]
        yield hint

        last = next


def import_clues(desc: TaskDesc, task: Task):
    clue_markdowns = list(read_hints_markdown(desc))
    
    for index, clue_markdown in enumerate(clue_markdowns):
        clue = TaskClue()
        clue.clue = clue_markdown
        clue.index = index
        clue.task = task
        clue.save()


def import_task(desc: TaskDesc, module: TaskModule):
    name = desc.name

    task = Task()
    task.name = name
    task.slug = desc.slug
    task.module = module
    task.points = 10

    if desc.desc is not None:
        task.desc = read_desc_markdown(desc)

    try:
        task.url = reverse(name)
    except NoReverseMatch:
        print("[ERROR] Mismatch between task view name and function name!")
        return False

    task.save()

    if desc.clues is not None:
        import_clues(desc, task)

    return True


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
                if import_task(task_desc, module) is False:
                    continue
