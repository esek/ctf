import subprocess

from typing import Any
from django.core.management.base import BaseCommand

from main.common import fetch_ctf_modules


class Command(BaseCommand):
    help = "Runs 'make' tasks for each of the registered modules"

    def handle(self, *args: Any, **options: Any) -> str | None:
        modules = fetch_ctf_modules()

        for module in modules:
            print(f"Running 'make' in \"{module.path}\":")

            result = subprocess.run(["make"], cwd=module.path, capture_output=True)
            print(result.stdout.strip())
