from __future__ import unicode_literals
from django.db import models
from base.models import Base
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyAW-1uN9-jxoiW0v2bP14KC5guXZea7Q3o')


class GameMapManager(models.Manager):
    def map_for_location(self, location, level):
        """
        Location should be an instance of base.Location.
        level should be an int.

        We need to figure out what to do when two maps overlap,
        are two of them visible at any one time? Or is a map built around a request
        and everything just has a location on the globe, so the map becomes what's around the player?
        Do we limit the edges of the map? what happens then if the user leaves?
        Do we make a map the size of the world?
        """
        pass

class GameMap(Base):
    """
    Game maps represent a physical area and combine with a dungeon level. Items and Actors live on
    a given map.
    """
    #Dungeon level, higher represents farther under ground.
    level = models.PositiveSmallIntegerField(default=1)

    top_right = models.ForeignKey("base.Location", related_name="game_map_top_right", blank=True, null=True)
    top_left = models.ForeignKey("base.Location", related_name="game_map_top_left", blank=True, null=True)
    bottom_right = models.ForeignKey("base.Location", related_name="game_map_bottom_right", blank=True, null=True)
    bottom_left = models.ForeignKey("base.Location", related_name="game_map_bottom_left", blank=True, null=True)

    objects = GameMapManager()

    def points_to_roads(self, points):
        """
        Points should be a list formatted like ["45.460627,-122.693437", "45.460907,-122.700917"]
        
        TODO interpret the response and get the data we need out of it.
        """
        return gmaps.nearest_roads(p)
