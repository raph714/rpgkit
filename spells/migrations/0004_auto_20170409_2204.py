# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 22:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spells', '0003_auto_20170409_2142'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spell',
            name='game_map',
        ),
        migrations.RemoveField(
            model_name='spell',
            name='location',
        ),
    ]