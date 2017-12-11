# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-10 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GameController',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(editable=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('monster_density', models.PositiveSmallIntegerField(default=10, help_text='Around about how many monsters should be generated for a particular map segment.')),
                ('monster_spawn_delay', models.PositiveSmallIntegerField(default=10, help_text='How often should monsters regenerate? (value in minutes)')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
