# Generated by Django 5.0.7 on 2024-08-26 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctef_core', '0005_task_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='slug',
            field=models.SlugField(default='test', max_length=500, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
