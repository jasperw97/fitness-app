# Generated by Django 5.0.1 on 2024-02-08 01:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_goalsmodel_workout_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.goalsmodel'),
        ),
    ]
