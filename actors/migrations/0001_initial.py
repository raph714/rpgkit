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
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('base_strength', models.PositiveSmallIntegerField()),
                ('base_dexterity', models.PositiveSmallIntegerField()),
                ('base_constitution', models.PositiveSmallIntegerField()),
                ('base_intelligence', models.PositiveSmallIntegerField()),
                ('base_wisdom', models.PositiveSmallIntegerField()),
                ('base_charisma', models.PositiveSmallIntegerField()),
                ('base_level', models.PositiveSmallIntegerField()),
                ('base_hp', models.PositiveSmallIntegerField()),
                ('base_mana', models.PositiveSmallIntegerField()),
                ('base_armor_class', models.PositiveSmallIntegerField()),
                ('base_max_carry_weight', models.PositiveSmallIntegerField(default=0)),
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
                ('affects', models.ManyToManyField(blank=True, related_name='actor_affects', to='affects.Affect')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]