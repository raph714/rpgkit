from __future__ import unicode_literals

from django.db import models
from base.models import Base

#This represents global settings for the game to be
#represented by an admin interface.
class GameController(Base):
    monster_density = models.PositiveSmallIntegerField(default=10, help_text="Around about how many monsters should be generated for a particular map segment.")
    monster_spawn_delay = models.PositiveSmallIntegerField(default=10, help_text="How often should monsters regenerate? (value in minutes)")