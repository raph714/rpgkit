from __future__ import unicode_literals

from django.db import models
from base.models import Base


class Condition(Base):
    affect_turns = models.PositiveSmallIntegerField()
    permanent = models.BooleanField()
