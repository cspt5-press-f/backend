# Generated by Django 3.0.3 on 2020-03-03 05:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0004_auto_20200229_0351'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='items',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]