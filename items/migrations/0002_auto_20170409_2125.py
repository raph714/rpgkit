# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 21:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='item',
            name='longitude',
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.Location'),
        ),
    ]
