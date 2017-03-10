from __future__ import unicode_literals

from django.db import models
from base.models import Base


class Actor(Base):
    """
    Attributes that do not include affects.
    """
    base_strength = models.PositiveSmallIntegerField(default=10)
    base_dexterity = models.PositiveSmallIntegerField(default=10)
    base_constitution = models.PositiveSmallIntegerField(default=10)
    base_intelligence = models.PositiveSmallIntegerField(default=10)
    base_wisdom = models.PositiveSmallIntegerField(default=10)
    base_charisma = models.PositiveSmallIntegerField(default=10)

    base_level = models.PositiveSmallIntegerField(default=1)
    base_hp = models.PositiveSmallIntegerField(default=10)
    base_mana = models.PositiveSmallIntegerField(default=10)
    base_armor_class = models.PositiveSmallIntegerField(default=10)

    base_max_carry_weight = models.PositiveSmallIntegerField(default=0)

    """
    These are the attributes after the modifying affects have been applied,
    so they don't need to be calculated all the time.
    """
    strength = models.PositiveSmallIntegerField(default=10)
    dexterity = models.PositiveSmallIntegerField(default=10)
    constitution = models.PositiveSmallIntegerField(default=10)
    intelligence = models.PositiveSmallIntegerField(default=10)
    wisdom = models.PositiveSmallIntegerField(default=10)
    charisma = models.PositiveSmallIntegerField(default=10)

    level = models.PositiveSmallIntegerField(default=1)
    hp = models.PositiveSmallIntegerField(default=10)
    mana = models.PositiveSmallIntegerField(default=10)
    armor_class = models.PositiveSmallIntegerField(default=10)

    max_carry_weight = models.PositiveSmallIntegerField(default=0)

    inventory = models.ManyToManyField("items.Item", related_name="actor_inventory", blank=True)
    wielding = models.ForeignKey("items.Weapon", related_name="actor_weapon", blank=True, null=True)
    wearing = models.ManyToManyField("items.Armor", related_name="actor_armor", blank=True)
    spells = models.ManyToManyField("spells.Spell", related_name="actor_spells", blank=True)

    sleeping = models.BooleanField(default=False)
    affects = models.ManyToManyField("affects.Affect", related_name="actor_affects", blank=True)

    def wield_weapon(self, item):
        """
        The user is trying to put something on. Figure out where it's supposed to go and put it on...

        We need to remove anything that occupies the slot that the thing is being wielded goes with,
        as well as verify that it can be used by this actor.
        """
        if self.wielding:
            self.affects.remove(*self.wielding.affects.all())

        self.wielding = item
        self.affects.add(*item.affects.all())
        self.save()

    def wield_armor(self, item):
        """
        """

    def sell_item(self):
        """
        Give the owner the value of the item, plus or minus any augments that other effects might have.
        """

    def cast_spell(self):
        """
        """
