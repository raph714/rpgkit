from __future__ import unicode_literals

from django.db import models


class Item(models.Model):
    die_set = models.ForeignKey("dice.DieSet", related_name="items")

    value = models.PositiveIntegerField()
