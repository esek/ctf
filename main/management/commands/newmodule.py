from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

from ...patches import patch_module

UNWANTED_ITEMS = ["admin", "tests", "models"]


class Command(BaseCommand):

    def initial_cleanup(self, module_name):
        for item in UNWANTED_ITEMS:
            os.remove(f"{module_name}/{item}.py")

    def handle(self, *args, **options):
        print("\nWelcome to the CTF module creation wizard!\n")

        def prompt_choice(choice_str: str, binary: bool = False) -> str | bool:
            print(f"{choice_str}{" (y/n)" if binary else ""}: ", end="")
            choice_str = input()

            if binary is False:
                return choice_str
            else:
                return choice_str == "y"

        title = prompt_choice("Title")
        use_makefile = prompt_choice("Does your module require a makefile?", True)

        module_name = title.lower().replace(" ", "_")

        call_command("startapp", module_name)

        self.initial_cleanup(module_name)
        patch_module(module_name, title, use_makefile)

        if use_makefile:
            # Create empty Makefile if requested.
            makefile_file = open(f"{module_name}/Makefile", "x")
            makefile_file.close()
