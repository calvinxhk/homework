# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-06 12:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('作业一', '0009_userinfo_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='boy',
        ),
        migrations.RemoveField(
            model_name='record',
            name='girl',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user_info',
        ),
        migrations.AddField(
            model_name='userboy',
            name='record',
            field=models.ManyToManyField(to='作业一.UserGirl'),
        ),
        migrations.DeleteModel(
            name='Record',
        ),
        migrations.DeleteModel(
            name='UserInfo',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
