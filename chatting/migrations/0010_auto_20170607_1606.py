# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 07:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatting', '0009_auto_20170605_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermessage',
            name='is_checked',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='userlogin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]