from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from base.models import Base, Location
import googlemaps
import datetime
from game_controller.models import GameController

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

        #1 degree latitude is about 69 miles, longitude varies based on lat. 
        #.01 degree is .69 miles, so that's what the grid will be based on.
        #truncate the lat and lon values that were passed in to get the grid origin point.
        lat = float(int(float(location.latitude)*100))/100
        lon = float(int(float(location.longitude)*100))/100
        newLoc, created = Location.objects.get_or_create(latitude=lat, longitude=lon, defaults={"latitude": lat, "longitude": lon})

        aMap, created = self.get_or_create(
            origin_location__latitude=lat, 
            origin_location__longitude=lon, 
            level=level, 
            defaults={"origin_location": newLoc, "level": level})

        return aMap


class GameMap(Base):
    """
    Game maps represent a physical area and combine with a dungeon level. Items and Actors live on
    a given map.
    """
    #Dungeon level, higher represents farther under ground.
    level = models.PositiveSmallIntegerField(default=1)
    origin_location = models.ForeignKey("base.Location", related_name="game_map_origin_location", blank=True, null=True)
    populate_date = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = GameMapManager()

    def __unicode__(self):
       return "id: %s lev: %s loc: %s" % (self.id, self.level, self.origin_location)

    def points_to_roads(self, points):
        """
        Points should be a list formatted like ["45.460627,-122.693437", "45.460907,-122.700917"] or [(40.714224, -73.961452), (41.714224, -72.961452)]
        
        TODO interpret the response and get the data we need out of it.
        """
        return gmaps.nearest_roads(p)

    def populate(self):
        """
        Figure out what is in the map
        """
        #get the game controller
        gc = GameController.objects.all()[0]

        now = timezone.now()
        print self.populate_date
        if now > self.populate_date + datetime.timedelta(minutes=gc.monster_spawn_delay):
            print "should update"
        

        
