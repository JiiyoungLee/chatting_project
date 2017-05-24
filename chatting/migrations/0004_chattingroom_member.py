# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 07:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chatting', '0003_auto_20170522_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='chattingroom',
            name='member',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
