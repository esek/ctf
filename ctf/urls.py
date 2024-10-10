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

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("main.urls")),
    path("admin/", admin.site.urls),
]

# Import and register all task views in installed CTF modules.
from main.common import fetch_ctf_modules
from main.views import config_hints_view

ctf_modules = fetch_ctf_modules()

for ctf_module in ctf_modules:
    import_module(f"{ctf_module.module.__name__}.views")

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
