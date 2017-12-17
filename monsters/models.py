from __future__ import unicode_literals
from django.db import models
from actors.models import Actor
from base.models import Base
from django.forms.models import model_to_dict

class MonsterType(Actor):
    """
    Template from which a monster instance is created and stuffed into a dungeon.
    These are technically actors, but are never actually placed on a map anywhere.
    """
    min_dungeon_level = models.PositiveSmallIntegerField(default=1)
    max_dungeon_level = models.PositiveSmallIntegerField(default=1)

    def generate(self, gameMap, location):
        #get a copy of the fields from this template we can apply to a monster
        kwargs = dict((f.name, getattr(self, f.name)) for f in self._meta.fields)

        #make sure to ditch the fields we don't want to copy!
        kwargs.pop('min_dungeon_level', None)
        kwargs.pop('max_dungeon_level', None)
        kwargs.pop('id', None)

        #make the monster
        m = Monster(**kwargs)
        m.location = location
        m.game_map = gameMap
        m.monster_type = self
        m.save()
        return m
 

class Monster(Actor):
    monster_type = models.ForeignKey(MonsterType, related_name="instances", blank=True, null=True)

    def __unicode__(self):
        return "pk: %s Level %s %s" % (self.pk, self.level, self.name)
