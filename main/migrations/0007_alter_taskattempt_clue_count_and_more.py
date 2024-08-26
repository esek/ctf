# Generated by Django 5.0.7 on 2024-08-26 21:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_task_slug_alter_task_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskattempt',
            name='clue_count',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='taskattempt',
            name='passed',
            field=models.BooleanField(default=False),
        ),
    ]
