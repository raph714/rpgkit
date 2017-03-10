from __future__ import unicode_literals

from django.db import models


class Item(models.Model):
    die_set = models.ForeignKey("dice.DieSet", related_name="items")
    affects = models.ManyToManyField("conditions.Condition", related_name="item_affects", blank=True)
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


class Wieldable(Item):
    """
    Parent class for any items that can be worn or held.
    """
    WEAPON = 'Weapon'
    SHIELD = 'Shield'
    ARMOR = 'Armor'
    GLOVES = 'Gloves'
    BOOTS = 'Boots'
    NECKLACE = 'Necklace'
    RING = 'Ring'

    ITEM_TYPE_CHOICES = (
        (WEAPON, WEAPON),
        (SHIELD, SHIELD),
        (ARMOR, ARMOR),
        (GLOVES, GLOVES),
        (BOOTS, BOOTS),
        (NECKLACE, NECKLACE),
        (RING, RING)
    )

    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES, db_index=True)


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