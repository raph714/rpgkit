from __future__ import unicode_literals

from django.db import models
from base import Base


class ActorClass(Base):
    strength = models.PositiveSmallIntegerField(min_value=1, max_value=100)
    dexterity = models.PositiveSmallIntegerField(min_value=1, max_value=100)
    constitution = models.PositiveSmallIntegerField(min_value=1, max_value=100)
    intelligence = models.PositiveSmallIntegerField(min_value=1, max_value=100)
    wisdom = models.PositiveSmallIntegerField(min_value=1, max_value=100)
    charisma = models.PositiveSmallIntegerField(min_value=1, max_value=100)

    level = models.PositiveSmallIntegerField(min_value=1, max_value=100)
    hp = models.PositiveSmallIntegerField(min_value=0)
    mana = models.PositiveSmallIntegerField(min_value=0)
    armor_class = models.PositiveSmallIntegerField(min_value=0)

    inventory = []

    right_hand = models.ForeignKey("items.Item", related_name="items")
    left_hand = None
    rings = []
    necklace = None
    wearing = None
    on_feet = None
    on_hands = None
    on_head = None

    sleeping = False
    illness = []
    effects = []
