# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0002_auto_20151211_1123'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_content', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Praise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('friend_id', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TalkMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.CharField(max_length=128)),
                ('content', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=100)),
                ('phone_num', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=16)),
                ('self_image_url', models.CharField(max_length=128)),
                ('avatar', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('access_token', models.CharField(blank=True, max_length=100)),
                ('refresh_token', models.CharField(blank=True, max_length=100)),
                ('expires_in', models.BigIntegerField(default=0, max_length=100)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.AddField(
            model_name='talkmsg',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User'),
        ),
        migrations.AddField(
            model_name='relation',
            name='self',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User'),
        ),
        migrations.AddField(
            model_name='praise',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User'),
        ),
        migrations.AddField(
            model_name='praise',
            name='talkmsg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TalkMsg'),
        ),
        migrations.AddField(
            model_name='comment',
            name='friend',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='talkmsg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.TalkMsg'),
        ),
    ]
