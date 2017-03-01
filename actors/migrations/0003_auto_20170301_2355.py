# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-01 23:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
        ('actors', '0002_actorclass_right_hand'),
    ]

    operations = [
        migrations.AddField(
            model_name='actorclass',
            name='inventory',
            field=models.ManyToManyField(null=True, related_name='inventory', to='items.Item'),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='left_hand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='left_hand', to='items.Item'),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='necklace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='necklace', to='items.Item'),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='on_feet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_feet', to='items.Item'),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='on_hands',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_hands', to='items.Item'),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='on_head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='on_head', to='items.Item'),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='rings',
            field=models.ManyToManyField(null=True, related_name='rings', to='items.Item'),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='sleeping',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='actorclass',
            name='wearing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wearing', to='items.Item'),
        ),
        migrations.AlterField(
            model_name='actorclass',
            name='right_hand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='right_hand', to='items.Item'),
        ),
    ]
