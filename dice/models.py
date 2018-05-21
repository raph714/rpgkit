from __future__ import unicode_literals
import random

from django.db import models


class DieSet(models.Model):
    number = models.PositiveSmallIntegerField()
    sides = models.PositiveSmallIntegerField()

    def roll_drop_lowest(self):
        rolls = self.get_rolls()
        rolls.sort()
        rolls.pop(0) #ditch lowest roll
        return sum(rolls)

    def get_rolls(self):
        rolls = []
        for die in range(0, self.number):
            rolls.append(random.randint(1, self.sides))
        return rolls

    @staticmethod
    def roll(num, sides):
        dice = DieSet()
        dice.number = num
        dice.sides = sides
        return sum(dice.get_rolls())
