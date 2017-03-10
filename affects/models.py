from __future__ import unicode_literals

from django.db import models
from base.models import Base


class Affect(Base):
    """
    A few kinds of affects:
        Damage modifier
        To hit modifier
        Actor stat modifier (benefit or curse)
        Damage of a certain kind (fire, frost, acid). Potential to damage other items actor carries. To be added later.
        Special vs certain kinds of monsters
    """
    affect_turns = models.PositiveSmallIntegerField(default=0)
    affect_turns_remaining = models.PositiveSmallIntegerField(default=0)
    permanent = models.BooleanField(default=False)
    curse = models.BooleanField(default=False)

    #These will be the +1, -4 etc number that get applied to the affected actor.
    modifier = models.SmallIntegerField(default=0)
    #String representation of the attribute that will be affected.
    attribute = models.CharField(max_length=100)

    def apply(self, item, actor):
        """
        Whatever this thing is going to do, it needs to be done here...
        They should be called whenever needed (when they are first applied, or
        when they affect someone who just got hit with one or something) and
        must be subclassed.
        """
        return None

