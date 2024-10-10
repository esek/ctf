from django.contrib import admin
from .models import TaskModule, Task, TaskAttempt, TaskClue

# Register your models here.
admin.site.register(TaskModule)
admin.site.register(Task)
admin.site.register(TaskAttempt)
admin.site.register(TaskClue)
