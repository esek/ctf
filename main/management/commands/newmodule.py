from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

UNWANTED_ITEMS = ["admin", "tests", "models"]


class Command(BaseCommand):

    def initial_cleanup(self, module_name):
        for item in UNWANTED_ITEMS:
            os.remove(f"{module_name}/{item}.py")

    def handle(self, *args, **options):
        print("\nWelcome to the CTF module creation wizard!\n")

        def prompt_choice(choice: str):
            print(f"{choice}: ", end="")
            return input()

        title = prompt_choice("Title")
        module_name = title.lower().replace(" ", "_")

        call_command("startapp", module_name)

        self.initial_cleanup(module_name)
