from typing import Any
from django.core.management.base import BaseCommand
import docker
import docker.errors

from ctef_core.common import fetch_ctf_modules
from ctef_core.management.commands._common import DOCKER_NETWORK_ID, module_container_name


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
                # Create container for image
                container = client.containers.get(module_container_name(module.name))
                container.stop()
                container.remove(v=True)
            except docker.errors.NotFound:
                print(f"No container online for module {module.name}")

        try:
            # Shutdown the network if it is still running.
            network = client.networks.get(DOCKER_NETWORK_ID)
            network.remove()
        except:
            print(f"Docker network {DOCKER_NETWORK_ID} is not running.")
