# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 11:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='friend',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='talkmsg',
        ),
        migrations.RemoveField(
            model_name='praise',
            name='friend',
        ),
        migrations.RemoveField(
            model_name='praise',
            name='talkmsg',
        ),
        migrations.RemoveField(
            model_name='relation',
            name='self',
        ),
        migrations.RemoveField(
            model_name='talkmsg',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Praise',
        ),
        migrations.DeleteModel(
            name='Relation',
        ),
        migrations.DeleteModel(
            name='TalkMsg',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]