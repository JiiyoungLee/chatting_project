# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 00:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chattingroom',
            name='room_name',
            field=models.CharField(default='Come and Have Fun With Me', max_length=100),
        ),
    ]
