from __future__ import unicode_literals

from django.db import models
from base.models import Base


class ActorClass(Base):
    strength = models.PositiveSmallIntegerField()
    dexterity = models.PositiveSmallIntegerField()
    constitution = models.PositiveSmallIntegerField()
    intelligence = models.PositiveSmallIntegerField()
    wisdom = models.PositiveSmallIntegerField()
    charisma = models.PositiveSmallIntegerField()

    level = models.PositiveSmallIntegerField()
    hp = models.PositiveSmallIntegerField()
    mana = models.PositiveSmallIntegerField()
    armor_class = models.PositiveSmallIntegerField()

    inventory = models.ManyToManyField("items.Item", related_name="inventory", null=True)

    right_hand = models.ForeignKey("items.Item", related_name="right_hand", null=True)
    left_hand = models.ForeignKey("items.Item", related_name="left_hand", null=True)
    rings = models.ManyToManyField("items.Item", related_name="rings", null=True)
    necklace = models.ForeignKey("items.Item", related_name="necklace", null=True)
    wearing = models.ForeignKey("items.Item", related_name="wearing", null=True)
    on_feet = models.ForeignKey("items.Item", related_name="on_feet", null=True)
    on_hands = models.ForeignKey("items.Item", related_name="on_hands", null=True)
    on_head = models.ForeignKey("items.Item", related_name="on_head", null=True)

    sleeping = models.BooleanField(default=False)
    illness = models.ManyToManyField("conditions.Condition", related_name="illness", null=True)
    affects = models.ManyToManyField("conditions.Condition", related_name="affects", null=True)
