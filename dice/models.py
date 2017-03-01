from __future__ import unicode_literals
import random

from django.db import models


class DieSet(models.Model):
    number = models.PositiveSmallIntegerField()
    sides = models.PositiveSmallIntegerField()

    def roll(self):
        roll = 0
        for die in range(0, self.number):
            roll = roll + random.randint(1, self.sides)
        return roll
