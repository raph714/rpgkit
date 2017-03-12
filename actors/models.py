from __future__ import unicode_literals

from django.db import models
from base.models import Base
from items.models import Armor, Jewelry


class Race(Base):
    """
    Race gives some bonuses to the Actor to which it applies.
    """
    affects = models.ManyToManyField("affects.Affect", related_name="race_affects", blank=True)


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

    base_resist_poison = models.PositiveSmallIntegerField(default=10)
    base_resist_fire = models.PositiveSmallIntegerField(default=10)
    base_resist_cold = models.PositiveSmallIntegerField(default=10)
    base_resist_acid = models.PositiveSmallIntegerField(default=10)
    base_resist_electricity = models.PositiveSmallIntegerField(default=10)

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

    resist_poison = models.PositiveSmallIntegerField(default=10)
    resist_fire = models.PositiveSmallIntegerField(default=10)
    resist_cold = models.PositiveSmallIntegerField(default=10)
    resist_acid = models.PositiveSmallIntegerField(default=10)

    level = models.PositiveSmallIntegerField(default=1)
    hp = models.PositiveSmallIntegerField(default=10)
    hp_max = models.PositiveSmallIntegerField(default=10)
    mana = models.PositiveSmallIntegerField(default=10)
    mana_max = models.PositiveSmallIntegerField(default=10)
    armor_class = models.PositiveSmallIntegerField(default=10)

    max_carry_weight = models.PositiveSmallIntegerField(default=0)
    current_carry_weight = models.PositiveSmallIntegerField(default=0)

    """
    The rest of these are independent of current level and do not need a base version.
    """
    experience_value = models.PositiveIntegerField(default=10)

    race = models.ForeignKey("actors.Race", related_name="actor", blank=True, null=True)

    inventory = models.ManyToManyField("items.Item", related_name="actor_inventory", blank=True)
    spells = models.ManyToManyField("spells.Spell", related_name="actor_spells", blank=True)

    weapon = models.OneToOneField("items.Weapon", related_name="actor_weapon", blank=True, null=True)
    range_weapon = models.OneToOneField("items.MissileWeapon", related_name="actor", blank=True, null=True)
    quiver = models.OneToOneField("items.Missile", related_name="actor", blank=True, null=True)

    armor = models.OneToOneField("items.Armor", related_name="actor_armor", limit_choices_to={'armor_type': Armor.ARMOR}, blank=True, null=True)
    helmet = models.OneToOneField("items.Armor", related_name="actor_helmet", limit_choices_to={'armor_type': Armor.HELMET}, blank=True, null=True)
    cloak = models.OneToOneField("items.Armor", related_name="actor_cloak", limit_choices_to={'armor_type': Armor.CLOAK}, blank=True, null=True)
    shoes = models.OneToOneField("items.Armor", related_name="actor_shoes", limit_choices_to={'armor_type': Armor.SHOES}, blank=True, null=True)
    gloves = models.OneToOneField("items.Armor", related_name="actor_gloves", limit_choices_to={'armor_type': Armor.GLOVES}, blank=True, null=True)
    pants = models.OneToOneField("items.Armor", related_name="actor_pants", limit_choices_to={'armor_type': Armor.PANTS}, blank=True, null=True)
    shield = models.OneToOneField("items.Armor", related_name="actor_shield", limit_choices_to={'armor_type': Armor.SHIELD}, blank=True, null=True)

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
        For each type, get the right slot, remove any affects that may be present from the current slot.
        """
        armor_qs = self.wearing.filter(armor_type=item.armor_type)
        if armor_qs.count() > 0:
            cur_wearing = armor_qs.all()
            for i in cur_wearing:
                self.affects.remove(*i.affects.all())

        self.wielding = item
        self.affects.add(*item.affects.all())
        self.save()

    def reset_attributes(self):
        """
        Set all of our attributes back to equal to the base attributes, usually when
        actor gains a level.
        """
        strength = base_strength
        dexterity = base_dexterity
        constitution = base_constitution
        intelligence = base_intelligence
        wisdom = base_wisdom
        charisma = base_charisma

        resist_poison = base_resist_poison
        resist_fire = base_resist_fire
        resist_cold = base_resist_cold
        resist_acid = base_resist_acid

        level = base_level
        hp = base_hp
        hp_max = base_hp
        mana = base_mana
        mana_max = base_mana
        armor_class = base_armor_class

        max_carry_weight = base_max_carry_weight

    def gain_level(self):
        """
        All we want to do here is recalculate our stats based on the new level and the race.
        """
        #Go through each affect on our race.
        for affect in self.race.affects.all():
            affect.apply(self)

        #Reset our attributes
        self.reset_attributes()

        #Now go through each affect from other stuff to calculate our modified attributes.
        for affect in self.affects.all():
            affect.apply(self)

    def update_weight(self):
        """
        Go through the inventory and add up all the weights and set the current_carry_weight
        """

    def pickup_item(self, item):
        """
        User wants to pick up an item, we need to add it to the inventory, and update carry weight.
        """

    def drop_item(self, item):
        """
        Take out of the inventory and update carry weight.
        """
