# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='praise',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='talkmsg',
            name='address',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='talkmsg',
            name='device',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='talkmsg',
            name='src',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
