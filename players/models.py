from __future__ import unicode_literals
from django.db import models
from actors.models import Actor
from base.models import Base

class PlayerMessageManager(models.Manager):
    def send_message(self, player, message):
        message = PlayerMessage()
        message.recipient = player
        message.name = "message to %s" % player.name
        message.description = description
        message.save()


class PlayerMessage(Base):
    """
    These are used for updates that should be retrieved on the API request after they are created, then
    subsequently deleted.
    """
    is_delivered = models.BooleanField(default=False)
    recipient = models.ForeignKey("players.Player", related_name="messages")

    objects = PlayerMessageManager()
 

class Race(Base):
    """
    Race gives some bonuses to the Actor to which it applies.
    """
    affects = models.ManyToManyField("affects.Affect", related_name="race_affects", blank=True)


class Class(Base):
    """
    Class gives some bonuses and allows use of some specialized items and spells.
    """
    affects = models.ManyToManyField("affects.Affect", related_name="class_affects", blank=True)


class Player(Actor):
    owner = models.ForeignKey('auth.User', related_name='players', blank=True, null=True)
    race = models.ForeignKey("players.Race", related_name="players", blank=True, null=True)
    actor_class = models.ForeignKey("players.Class", related_name="players", blank=True, null=True)

    def __unicode__(self):
       return "%s - Level %s %s %s" % (self.owner.username, self.level, self.race.name, self.actor_class.name)

    def save(self, *args, **kwargs):    
        self.display_char = "@"
        super(Player, self).save(*args, **kwargs)
