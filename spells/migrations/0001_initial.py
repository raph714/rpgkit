# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 05:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('affects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Spell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('min_level', models.PositiveSmallIntegerField(default=1)),
                ('mana_cost', models.PositiveSmallIntegerField(default=1)),
                ('max_range', models.PositiveSmallIntegerField(default=10)),
                ('affected_area', models.PositiveSmallIntegerField(default=0)),
                ('affects', models.ManyToManyField(blank=True, related_name='spell_affects', to='affects.Affect')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
