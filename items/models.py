from __future__ import unicode_literals

from django.db import models


class Item(models.Model):
    owner = models.ForeignKey("actors.Actor", related_name="items")
    die_set = models.ForeignKey("dice.DieSet", related_name="items", null=True, blank=True)
    affects = models.ManyToManyField("affects.Affect", related_name="item_affects", blank=True)
    value = models.PositiveIntegerField(default=0)
    weight = models.PositiveSmallIntegerField(default=0)

    def apply_affects(self, actor):
        """
        Any time an item is used, or equipped, the affects need to be applied to whoever used the thing.
        """

    def remove_affects(self, actor):
        """
        This item was removed, or discarded, and it's associated affects should be removed from the actor.
        """


class Weapon(Item):
    """
    These things can hurt!
    """
    hit_affects = models.ManyToManyField("affects.Affect", related_name="weapon_affects", blank=True)
    two_handed = models.BooleanField(default=False)


class Armor(Item):
    """
    Protection for the wearer
    """
    SHIELD = 'Shield'
    ARMOR = 'Armor'
    GLOVES = 'Gloves'
    BOOTS = 'Boots'
    NECKLACE = 'Necklace'
    RING = 'Ring'

    ITEM_TYPE_CHOICES = (
        (SHIELD, SHIELD),
        (ARMOR, ARMOR),
        (GLOVES, GLOVES),
        (BOOTS, BOOTS),
        (NECKLACE, NECKLACE),
        (RING, RING)
    )

    armor_class = models.PositiveSmallIntegerField()
    armor_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, db_index=True)


class Missile(Item):
    """
    Anything that can be thrown or shot.
    """
    ARROW = 'Arrow'
    BOLT = 'Bolt'
    STONE = 'Stone'

    ITEM_TYPE_CHOICES = (
        (ARROW, ARROW),
        (BOLT, BOLT),
        (STONE, STONE)
    )
    missile_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, db_index=True)


class Scroll(Item):
    """
    Scrolls can be used to cast or learn a spell. If the user is a magic user who meets the
    minimum requirements for casting the spell, the scroll can be learned instead of used.
    """
    spell = models.ForeignKey("spells.Spell", related_name="scrolls")

