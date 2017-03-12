from __future__ import unicode_literals

from django.db import models
from base.models import BaseOffense


class Item(BaseOffense):
    owner = models.ForeignKey("actors.Actor", related_name="items")
    die_set = models.ForeignKey("dice.DieSet", related_name="items", null=True, blank=True)
    holder_affects = models.ManyToManyField("affects.Affect", related_name="item_holder_affects", blank=True)
    hit_affects = models.ManyToManyField("affects.Affect", related_name="item_hit_affects", blank=True)
    value = models.PositiveIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(default=0)
    for_sale = models.BooleanField(default=False)


class Weapon(Item):
    """
    These things can hurt!
    """
    two_handed = models.BooleanField(default=False)


class MissileWeapon(Weapon):
    """
    Bows n stuff.
    """
    BOW = 'Bow'
    CROSSBOW = 'Crossbow'
    SLING = 'Sling'

    WEAPON_TYPES = (
        (BOW, BOW),
        (CROSSBOW, CROSSBOW),
        (SLING, SLING)
    )

    missile_type = models.CharField(max_length=10, choices=WEAPON_TYPES, default=BOW, db_index=True)
    missile_range = models.PositiveSmallIntegerField(default=10)


class Missile(Item):
    """
    Anything that can be thrown or shot.
    """
    ARROW = 'Arrow'
    BOLT = 'Bolt'
    STONE = 'Stone'

    MISSILE_TYPES = (
        (ARROW, ARROW),
        (BOLT, BOLT),
        (STONE, STONE)
    )

    missile_type = models.CharField(max_length=10, choices=MISSILE_TYPES, default=ARROW, db_index=True)
    usable_weapon_type = models.CharField(max_length=10, choices=MissileWeapon.WEAPON_TYPES, default=ARROW, db_index=True)


class Armor(Item):
    """
    Protection for the wearer
    """
    HELMET = 'Helmet'
    CLOAK = 'Cloak'
    ARMOR = 'Armor'
    SHOES = 'Shoes'
    GLOVES = 'Gloves'
    PANTS = 'Pants'
    SHIELD = 'Shield'

    ARMOR_TYPES = (
        (HELMET, HELMET),
        (CLOAK, CLOAK),
        (ARMOR, ARMOR),
        (SHOES, SHOES),
        (GLOVES, GLOVES),
        (PANTS, PANTS),
        (SHIELD, SHIELD)
    )

    armor_class = models.PositiveSmallIntegerField(default=0)
    armor_type = models.CharField(max_length=10, choices=ARMOR_TYPES, default=ARMOR, db_index=True)


class Jewelry(Item):
    """
    Magical little baubles
    """
    RING = 'Ring'
    NECKLACE = 'Necklace'
    CROWN = 'Crown'

    JEWELRY_TYPES = (
        (RING, RING),
        (NECKLACE, NECKLACE),
        (CROWN, CROWN)
    )

    jewelry_type = models.CharField(max_length=10, choices=JEWELRY_TYPES, default=RING, db_index=True)


class Scroll(Item):
    """
    Scrolls can be used to cast or learn a spell. If the user is a magic user who meets the
    minimum requirements for casting the spell, the scroll can be learned instead of used.
    """
    spell = models.ForeignKey("spells.Spell", related_name="scrolls")

    #To learn the spell, reader must be of a certain level.
    min_level = models.PositiveSmallIntegerField(default=0)

