"""
URL configuration for ctf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from importlib import import_module
import docker

from django.contrib import admin
from django.urls import path, include, re_path

import docker.errors
from revproxy.views import ProxyView

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
]

# Import and register all task views in installed CTF modules.
from main.common import fetch_ctf_modules
from main.views import config_hints_view
from main.management.commands.common import module_container_name

client = docker.from_env()

ctf_modules = fetch_ctf_modules()

for ctf_module in ctf_modules:
    module_name = ctf_module.module.__name__
    import_module(f"{module_name}.views")

    try:
        if ctf_module.use_docker:
            container_name = module_container_name(module_name)

            container = client.containers.get(container_name)
            IPAddress = container.attrs["NetworkSettings"]["IPAddress"]

            urlpatterns.append(
                re_path(
                    f"envs/{module_name}/(?P<path>.*)",
                    ProxyView.as_view(upstream=f"http://{IPAddress}:8080"),
                )
            )
    except (AttributeError, docker.errors.NotFound) as e:
        pass
    
# Import MODULE_TASKS after being populated by the previous section imports.
from main.decorators import MODULE_TASKS

for module, tasks in MODULE_TASKS.items():
    for task in tasks:
        urlpatterns.append(
            path(f"{module}/{task.slug}", view=task.view, name=task.name)
        )

        # Add the corresponding hints page for the task.
        urlpatterns.append(
            path(
                f"{module}/{task.slug}/hints",
                view=config_hints_view(task),
                name=f"{task.name}_hints",
            )
        )
