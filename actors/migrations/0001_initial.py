# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-04 00:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conditions', '0001_initial'),
        ('items', '0004_missile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('strength', models.PositiveSmallIntegerField()),
                ('dexterity', models.PositiveSmallIntegerField()),
                ('constitution', models.PositiveSmallIntegerField()),
                ('intelligence', models.PositiveSmallIntegerField()),
                ('wisdom', models.PositiveSmallIntegerField()),
                ('charisma', models.PositiveSmallIntegerField()),
                ('level', models.PositiveSmallIntegerField()),
                ('hp', models.PositiveSmallIntegerField()),
                ('mana', models.PositiveSmallIntegerField()),
                ('armor_class', models.PositiveSmallIntegerField()),
                ('max_carry_weight', models.PositiveSmallIntegerField(default=0)),
                ('sleeping', models.BooleanField(default=False)),
                ('affects', models.ManyToManyField(blank=True, related_name='actors_affects', to='conditions.Condition')),
                ('inventory', models.ManyToManyField(blank=True, related_name='actors_inventory', to='items.Item')),
                ('wielding', models.ManyToManyField(blank=True, related_name='actors_weilding', to='items.Wieldable')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
