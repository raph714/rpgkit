from __future__ import unicode_literals

from django.db import models
from base.models import Base


class Spell(Base):
    min_level = models.PositiveSmallIntegerField(default=1)
    mana_cost = models.PositiveSmallIntegerField(default=1)
    #distance in meters
    max_range = models.PositiveSmallIntegerField(default=10)
    affected_area = models.PositiveSmallIntegerField(default=0)
    affects = models.ManyToManyField("affects.Affect", related_name="spell_affects", blank=True)
