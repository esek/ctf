from typing import Any
from django.core.management.base import BaseCommand
import docker
import docker.errors

from main.common import fetch_ctf_modules


class Command(BaseCommand):
    help = "Launches built containers for each activate CTF module."

    def handle(self, *args: Any, **options: Any) -> str | None:
        docker_modules = fetch_ctf_modules("use_docker")

        # Return if no docker modules are present.
        if not docker_modules:
            return

        client = docker.from_env()

        for module in docker_modules:
            try:
                # Get pre-built image for module
                image = client.images.get(f"ctf/{module.name}_env")
                # Create container for image
                client.containers.run(image, name=f"ctf_{module.name}_env")
            except docker.errors.ImageNotFound:
                print(f"No pre-built image was found for {module.name}")
