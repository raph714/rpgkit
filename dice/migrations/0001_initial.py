# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 05:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DieSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField()),
                ('sides', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
