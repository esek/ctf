from typing import Any
from django.core.management.base import BaseCommand

from main.models import TaskModule

class Command(BaseCommand):
    help = 'Drops all database information reqarding tasks and tasks modules.'

    def handle(self, *args: Any, **options: Any) -> str | None:
        TaskModule.objects.all().delete()