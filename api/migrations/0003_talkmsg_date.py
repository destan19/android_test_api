# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 17:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20151214_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='talkmsg',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]