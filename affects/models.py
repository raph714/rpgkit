from __future__ import unicode_literals

from django.db import models
from base.models import Base
from actors.models import Actor


class Affect(Base):
    """
    A few kinds of affects:
        Damage modifier
        To hit modifier
        Actor stat modifier (benefit or curse)
        Damage of a certain kind (fire, frost, acid). Potential to damage other items actor carries. To be added later.
        Special vs certain kinds of monsters
    """
    ADD = 0
    MULTIPLY = 1

    AFFECT_TYPE_CHOICES = (
        (ADD, "Add"),
        (MULTIPLY, "Multiply")
    )

    affect_turns = models.PositiveSmallIntegerField(default=0)
    affect_turns_remaining = models.PositiveSmallIntegerField(default=0)
    permanent = models.BooleanField(default=False)
    curse = models.BooleanField(default=False)
    
    #determine whether to add or multiply
    affect_type = models.CharField(max_length=10, choices=AFFECT_TYPE_CHOICES, default=ADD, db_index=True)

    #These will be the +1, -4 etc number that get applied to the affected actor.
    modifier = models.FloatField(default=0)

    #String representation of the attribute that will be affected.
    attribute = models.CharField(max_length=100)

    def apply(self, obj):
        """
        Whatever this thing is going to do, it needs to be done here...
        They should be called whenever needed (when they are first applied, or
        when they affect someone who just got hit with one or something).
        """
        if hasattr(obj, self.attribute):
            cur_val = getattr(obj, self.attribute)
            if self.affect_type == ADD:
                new_val = cur_val + self.modifier
            else:
                new_val = cur_val * self.modifier

            setattr(obj, self.attribute, new_val)

    def remove(self, obj):
        if hasattr(obj, self.attribute):
            cur_val = getattr(obj. self.attribute)
            if self.affect_type == ADD:
                new_val = cur_val - self.modifier
            else:
                new_val = cur_val / self.modifier

            setattr(obj, self.attribute, new_val)
