# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 04:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0005_actor_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actors', to=settings.AUTH_USER_MODEL),
        ),
    ]