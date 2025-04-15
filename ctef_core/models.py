from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from .fields import TaskSecretField

MAX_CLUE_COUNT = 10
MAX_TASK_POINTS = 100


# Create your models here.
class Competition(models.Model):
    name = models.CharField(max_length=500, unique=True, null=False)

    def __str__(self):
        return f'Competition "{self.name}"'


class CompetitionParticipation(models.Model):
    score = models.PositiveSmallIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}\'s participation in competition "{self.competition.name}"'


class TaskModule(models.Model):
    """A grouping of tasks with a common theme or technique."""

    name = models.CharField(max_length=500, unique=True, null=False)
    title = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name + f" ({self.title})"


class Task(models.Model):
    name = models.CharField(max_length=500, null=False, unique=True)
    slug = models.SlugField(max_length=500, null=False, unique=True)
    url = models.CharField(max_length=500)

    points = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(MAX_TASK_POINTS)]
    )

    desc = models.TextField(blank=True)

    module = models.ForeignKey(TaskModule, on_delete=models.CASCADE)
    secret = TaskSecretField()

    def __str__(self) -> str:
        return self.name


class TaskClue(models.Model):
    clue = models.TextField()
    index = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(MAX_CLUE_COUNT)]
    )
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskAttempt(models.Model):
    clue_count = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(MAX_CLUE_COUNT)], default=0
    )
    points = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(MAX_TASK_POINTS)]
    )
    passed = models.BooleanField(default=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, null=None)

    def __str__(self) -> str:
        return f"{self.user.username}'s attempt on task '{self.task.name}'"
