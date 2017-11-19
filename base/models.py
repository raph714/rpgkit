from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify


class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)


class Base(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(db_index=True, editable=False)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Base, self).save(*args, **kwargs)

    def __unicode__(self):
       return self.name


class BaseGameObject(Base):
    """
    These things exist in the world. We need to know where they are,
    and on which game map.
    """
    location = models.ForeignKey("base.Location", blank=True, null=True)
    game_map = models.ForeignKey("game_map.GameMap", blank=True, null=True)
    game_map_level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):    
        super(Base, self).save(*args, **kwargs)

    def update_location(self, location):
        """
        Update the location and update the game map for the actor as necessary.
        """
        from game_map.models import GameMap
        self.location = location
        self.game_map = GameMap.objects.map_for_location(self.location, self.game_map_level)
        self.save()
