from typing import Any
from django.core.management.base import BaseCommand
import docker
import docker.errors

from main.common import fetch_ctf_modules
from main.management.commands.common import DOCKER_NETWORK_ID, module_container_name
from main.models import Task, TaskModule


class Command(BaseCommand):
    help = "Launches built containers for each activate CTF module."

    def handle(self, *args: Any, **options: Any) -> str | None:
        docker_modules = fetch_ctf_modules("use_docker")

        # Return if no docker modules are present.
        if not docker_modules:
            return

        client = docker.from_env()

        try:
            network = client.networks.get(DOCKER_NETWORK_ID)
        except:
            network = client.networks.create(DOCKER_NETWORK_ID)

        for module in docker_modules:
            task_module = TaskModule.objects.get(name=module.name)
            module_tasks = Task.objects.filter(module=task_module)

            secret_env = {
                f"CTF_SECRET_{task.slug}": task.secret for task in module_tasks
            }

            try:
                # Get pre-built image for module
                image = client.images.get(f"ctf/{module.name}_env")
                # Create container for image
                # Note "Detach" to continue python code execution i.e. fire and forget.
                container_name = module_container_name(module.name)
                client.containers.run(
                    image, name=container_name, detach=True, environment=secret_env
                )

                # Connect the launched container to the network
                network.connect(container_name)
            except docker.errors.ImageNotFound:
                print(f"No pre-built image was found for {module.name}")
