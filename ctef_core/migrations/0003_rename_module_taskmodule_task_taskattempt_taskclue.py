# Generated by Django 5.0.7 on 2024-08-06 14:03

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctef_core', '0002_alter_module_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Module',
            new_name='TaskModule',
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('points', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctef_core.taskmodule')),
            ],
        ),
        migrations.CreateModel(
            name='TaskAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clue_count', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('points', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('passed', models.BooleanField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctef_core.task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TaskClue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clue', models.TextField()),
                ('index', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10)])),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctef_core.task')),
            ],
        ),
    ]
