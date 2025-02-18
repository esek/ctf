import subprocess
import docker
from typing import Any
from django.core.management.base import BaseCommand
import json

from ctef_core.common import fetch_ctf_modules


class Command(BaseCommand):
    help = "Runs 'make' tasks for each of the registered modules"

    def handle(self, *args: Any, **options: Any) -> str | None:
        make_modules = fetch_ctf_modules("use_makefile")

        for module in make_modules:
            print(f"Running 'make' in \"{module.path}\":")

            result = subprocess.run(["make"], cwd=module.path, capture_output=True)
            print(result.stdout.strip())

        docker_modules = fetch_ctf_modules("use_docker")

        if docker_modules:
            client = docker.from_env()

            for module in docker_modules:
                # Build the docker image for each module
                for output in client.api.build(
                    path=module.path, tag=f"ctef/{module.name}_env"
                ):
                    line_json = output.decode("utf-8")
                    line = json.loads(line_json)

                    if "stream" in line:
                        print(line["stream"])
