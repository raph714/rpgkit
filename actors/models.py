from __future__ import unicode_literals

from django.db import models
from base.models import Base, BaseGameObject
from items.models import Armor, Jewelry
from dice.models import DieSet


class Actor(BaseGameObject):
    """
    Attributes that do not include affects.
    """
    base_strength = models.PositiveSmallIntegerField(default=10)
    base_dexterity = models.PositiveSmallIntegerField(default=10)
    base_constitution = models.PositiveSmallIntegerField(default=10)
    base_intelligence = models.PositiveSmallIntegerField(default=10)
    base_wisdom = models.PositiveSmallIntegerField(default=10)
    base_charisma = models.PositiveSmallIntegerField(default=10)

    base_poison_resist = models.PositiveSmallIntegerField(default=10)
    base_fire_resist = models.PositiveSmallIntegerField(default=10)
    base_cold_resist = models.PositiveSmallIntegerField(default=10)
    base_acid_resist = models.PositiveSmallIntegerField(default=10)
    base_electricity_resist = models.PositiveSmallIntegerField(default=10)

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

    poison_resist = models.PositiveSmallIntegerField(default=10)
    fire_resist = models.PositiveSmallIntegerField(default=10)
    cold_resist = models.PositiveSmallIntegerField(default=10)
    acid_resist = models.PositiveSmallIntegerField(default=10)
    electricity_resist = models.PositiveSmallIntegerField(default=10)

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
    tohit_bonus_melee = models.PositiveSmallIntegerField(default=0)
    tohit_bonus_range = models.PositiveSmallIntegerField(default=0)
    damage_bonus_melee = models.PositiveSmallIntegerField(default=0)
    damage_bonus_range = models.PositiveSmallIntegerField(default=0)

    #Special kinds of damage that are done on top of, or instead of, regular attack damage.
    damage_bonus_poison = models.PositiveSmallIntegerField(default=0)
    damage_bonus_fire = models.PositiveSmallIntegerField(default=0)
    damage_bonus_cold = models.PositiveSmallIntegerField(default=0)
    damage_bonus_acid = models.PositiveSmallIntegerField(default=0)
    damage_bonus_electricity = models.PositiveSmallIntegerField(default=0)

    experience_earned = models.PositiveIntegerField(default=0)
    experience_to_level = models.PositiveIntegerField(default=0)

    #Were this actor to be killed, how much experience does the victor get?
    experience_value = models.PositiveIntegerField(default=10)

    inventory = models.ManyToManyField("items.Item", related_name="%(class)s_inventory", blank=True)
    spells = models.ManyToManyField("spells.Spell", related_name="%(class)s_spells", blank=True)

    weapon = models.OneToOneField("items.Weapon", related_name="%(class)s_weapon", blank=True, null=True)
    range_weapon = models.OneToOneField("items.MissileWeapon", related_name="%(class)s", blank=True, null=True)
    quiver = models.OneToOneField("items.Missile", related_name="%(class)s", blank=True, null=True)

    armor = models.OneToOneField("items.Armor", related_name="%(class)s_armor", limit_choices_to={'armor_type': Armor.ARMOR}, blank=True, null=True)
    helmet = models.OneToOneField("items.Armor", related_name="%(class)s_helmet", limit_choices_to={'armor_type': Armor.HELMET}, blank=True, null=True)
    cloak = models.OneToOneField("items.Armor", related_name="%(class)s_cloak", limit_choices_to={'armor_type': Armor.CLOAK}, blank=True, null=True)
    shoes = models.OneToOneField("items.Armor", related_name="%(class)s_shoes", limit_choices_to={'armor_type': Armor.SHOES}, blank=True, null=True)
    gloves = models.OneToOneField("items.Armor", related_name="%(class)s_gloves", limit_choices_to={'armor_type': Armor.GLOVES}, blank=True, null=True)
    pants = models.OneToOneField("items.Armor", related_name="%(class)s_pants", limit_choices_to={'armor_type': Armor.PANTS}, blank=True, null=True)
    shield = models.OneToOneField("items.Armor", related_name="%(class)s_shield", limit_choices_to={'armor_type': Armor.SHIELD}, blank=True, null=True)

    sleeping = models.BooleanField(default=False)
    affects = models.ManyToManyField("affects.Affect", related_name="%(class)s_affects", blank=True)

    def __unicode__(self):
       return "Level %s %s" % (self.level, self.name)

    class Meta:
        abstract = True

    def apply_affects(self, affects):
        """
        Activate new affects and add them to the relationship with this actor.
        Affects must be passed in as an iterable.
        """
        for affect in affects:
            affect.apply(self)
            self.affects.add(affect)

    def remove_affects(self, affects):
        """
        Deactivate and remove a list of affects.
        """
        for affect in affects:
            affect.remove(self)
            self.affects.remove(affect)

    def wield_weapon(self, item):
        """
        The user is trying to put something on. Figure out where it's supposed to go and put it on...

        We need to remove anything that occupies the slot that the thing is being wielded goes with,
        as well as verify that it can be used by this actor.
        """
        if self.wielding:
            self.remove_affects(*self.wielding.affects.all())

        self.wielding = item
        self.apply_affects(*item.affects.all())
        self.save()

    def wield_armor(self, item):
        """
        For each type, get the right slot, remove any affects that may be present from the current slot.
        """
        armor_type = item.armor_type

        if armor_type == Armor.ARMOR:
            if self.armor:
                self.remove_affects(*self.armor.affects.all())
            self.armor = item
        elif armor_type == Armor.HELMET:
            if self.helmet:
                self.remove_affects(*self.helmet.affects.all())
            self.helmet = item
        elif armor_type == Armor.CLOAK:
            if self.cloak:
                self.remove_affects(*self.cloak.affects.all())
            self.cloak = item
        elif armor_type == Armor.SHOES:
            if self.shoes:
                self.remove_affects(*self.shoes.affects.all())
            self.shoes = item
        elif armor_type == Armor.GLOVES:
            if self.gloves:
                self.remove_affects(*self.gloves.affects.all())
            self.gloves = item
        elif armor_type == Armor.PANTS:
            if self.pants:
                self.remove_affects(*self.pants.affects.all())
            self.pants = item
        elif armor_type == Armor.SHIELD:
            if self.shield:
                self.remove_affects(*self.shield.affects.all())
            self.shield = item

        self.apply_affects(*item.affects.all())
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

        poison_resist = base_poison_resist
        fire_resist = base_fire_resist
        cold_resist = base_cold_resist
        acid_resist = base_acid_resist

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
        self.apply_affects(*self.affects.all())

        #set new experience goal.

    def update_weight(self):
        """
        Go through the inventory and add up all the weights and set the current_carry_weight
        """
        new_weight = 0
        for item in self.items.all():
            new_weight += item.weight
        self.current_carry_weight = new_weight
        self.save()

    def pickup_item(self, item):
        """
        User wants to pick up an item, we need to add it to the inventory, and update carry weight.
        """
        self.inventory.add(item)
        self.update_weight()

        if self.current_carry_weight > self.max_carry_weight:
            overweight = self.current_carry_weight - self.max_carry_weight
            self.inventory.remove(item)

            ActorMessage.objects.send_message(
                actor=a, 
                description="You need to get rid of %s kilos from your inventory before you can pick this item up." % overweight
            )

        self.save()

    def drop_item(self, item):
        """
        Take out of the inventory and update carry weight.
        """
        self.inventory.remove(item)
        self.update_weight()
        save()

        #TODO put it back on the map? or just destroy it?

    def attack_melee(self, actor):
        if self.hits_melee(actor):
            return self.deal_melee_damage(actor)
        else:
            return "You missed %s." % actor.name

    def hits_melee(self, actor):
        #get a die roll
        roll = DieSet.roll(1, 20)
        #add to hit bonus
        roll += self.tohit_bonus_melee
        return roll >= actor.armor_class

    def deal_melee_damage(self, actor):
        """
        If we're not holding a weapon, just assume that we are punching.
        Punching is 2 damage.

        returns message to be sent back to player
        """
        damage = 2
        if self.weapon:
            damage = self.weapon.get_roll()

        damage += self.damage_bonus_melee

        message = actor.take_melee_damage(damage)
        message += actor.take_bonus_damage(self)

        #Now that the damage has been done, check to see if the other guy is dead!
        if actor.check_killed():
            message += "%s killed %s." % (self.name, actor.name)

        self.save()
        actor.save()

        return message

    def take_bonus_damage(self, actor):
        """
        Here we're just going to subtract the resistance bonus damage per type from the attacker's,
        any leftover does damage.

        We're not going to save at the end of this because the caller should save this object.

        TODO, see notes in the comments.
        """
        total_damage = 0
        message = []
        if actor.damage_bonus_electricity > self.electricity_resist:
            dam = actor.damage_bonus_electricity - self.electricity_resist
            total_damage += dam
            message.append("+ %s electricity damage" % dam)
        if actor.damage_bonus_fire > self.fire_resist:
            dam = actor.damage_bonus_fire - self.fire_resist
            total_damage += dam
            message.append("+ %s fire damage" % dam)
            #go through our pack and see if anything is flammable and roll to see if it burns.
        if actor.damage_bonus_cold > self.cold_resist:
            dam = actor.damage_bonus_cold - self.cold_resist
            total_damage += dam
            message.append("+ %s cold damage" % dam)
        if actor.damage_bonus_acid > self.acid_resist:
            dam = actor.damage_bonus_acid - self.acid_resist
            total_damage += dam
            message.append("+ %s acid damage" % dam)
            #go through our armor and see if something should be damaged by acid.
        if actor.damage_bonus_poison > self.poison_resist:
            dam = actor.damage_bonus_poison - self.poison_resist
            total_damage += dam
            message.append("+ %s poison damage" % dam)
            #check and see if we're poisoned.
        self.hp -= total_damage
        #figure out if we're dead or not!

        return ', '.join(message)

    def take_melee_damage(self, damage):
        self.hp -= damage
        return "%s was dealt %s damage." % (self.name, damage)

    def check_killed(self):
        """
        See if we're dead. Return a bool.
        """
        if self.hp <= 0:
            return True
        return False

    def roll_stats(self):
        """
        We're going to roll 4d6, drop the lowest for each stat.
        """
        dice = DieSet()
        dice.number = 4
        dice.sides = 6
        stats = {}
        stats["str"] = dice.roll_drop_lowest()
        stats["dex"] = dice.roll_drop_lowest()
        stats["int"] = dice.roll_drop_lowest()
        stats["con"] = dice.roll_drop_lowest()
        stats["cha"] = dice.roll_drop_lowest()
        stats["wis"] = dice.roll_drop_lowest()
        return stats

    def distance_to(self, actor):
        """
        Returns distance in meters.
        """
        return self.location.distance_to(actor.location)

    def can_melee(self, actor):
        return self.distance_to(actor) < 10
