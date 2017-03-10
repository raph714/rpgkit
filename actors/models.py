from __future__ import unicode_literals

from django.db import models
from base.models import Base


class Actor(Base):

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

    max_carry_weight = models.PositiveSmallIntegerField(default=0)

    inventory = models.ManyToManyField("items.Item", related_name="actors_inventory", blank=True)
    wielding = models.ManyToManyField("items.Wieldable", related_name="actors_weilding", blank=True)

    sleeping = models.BooleanField(default=False)
    affects = models.ManyToManyField("conditions.Condition", related_name="actors_affects", blank=True)

    def wield(self, item):
        """
        The user is trying to put something on. Figure out where it's supposed to go and put it on...

        We need to remove anything that occupies the slot that the thing is being wielded goes with,
        as well as verify that it can be used by this actor.
        """
