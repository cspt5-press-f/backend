# Generated by Django 3.0.3 on 2020-03-03 05:26

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0005_player_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='currentRoom',
        ),
        migrations.AddField(
            model_name='player',
            name='coordinates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=2),
        ),
    ]
