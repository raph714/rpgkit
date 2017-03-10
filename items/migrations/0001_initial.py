# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-10 05:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('actors', '0001_initial'),
        ('dice', '0001_initial'),
        ('spells', '0001_initial'),
        ('affects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(default=0)),
                ('weight', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Armor',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.Item')),
                ('armor_class', models.PositiveSmallIntegerField()),
                ('armor_type', models.CharField(choices=[('Shield', 'Shield'), ('Armor', 'Armor'), ('Gloves', 'Gloves'), ('Boots', 'Boots'), ('Necklace', 'Necklace'), ('Ring', 'Ring')], db_index=True, max_length=10)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='Missile',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.Item')),
                ('missile_type', models.CharField(choices=[('Arrow', 'Arrow'), ('Bolt', 'Bolt'), ('Stone', 'Stone')], db_index=True, max_length=10)),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='Scroll',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.Item')),
                ('spell', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scrolls', to='spells.Spell')),
            ],
            bases=('items.item',),
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='items.Item')),
                ('two_handed', models.BooleanField(default=False)),
                ('hit_affects', models.ManyToManyField(blank=True, related_name='weapon_affects', to='affects.Affect')),
            ],
            bases=('items.item',),
        ),
        migrations.AddField(
            model_name='item',
            name='affects',
            field=models.ManyToManyField(blank=True, related_name='item_affects', to='affects.Affect'),
        ),
        migrations.AddField(
            model_name='item',
            name='die_set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='dice.DieSet'),
        ),
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='actors.Actor'),
        ),
    ]
