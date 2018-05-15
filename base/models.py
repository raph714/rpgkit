from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
import googlemaps
import random
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)


class LocationManager(models.Manager):
    def map_origin_point(self, loc):
        """
        1 degree latitude is about 69 miles, longitude varies based on lat. 
        .01 degree is .69 miles, so that's what the grid will be based on.
        truncate the lat and lon values that were passed in to get the grid origin point.
        """
        lat = Location.snap_to_grid(loc.latitude)
        lon = Location.snap_to_grid(loc.longitude)
        newLoc, created = self.get_or_create(latitude=lat, longitude=lon, defaults={"latitude": lat, "longitude": lon})
        return newLoc

    def map_top_right_point(self, loc):
        """
        Returns the corresponding opposite corner from the origin point in which this location exists.
        
        """
        lat = Location.next_grid_point(loc.latitude)
        lon = Location.next_grid_point(loc.longitude)
        newLoc, created = self.get_or_create(latitude=lat, longitude=lon, defaults={"latitude": lat, "longitude": lon})
        return newLoc

    def existing_locations(self, startLoc, endLoc):
        """
        Returns a list of locations for a given box determined by two locations.
        """
        existingLocations = None

        if startLoc.latitude < 0 and startLoc.longitude < 0:
            existingLocations = self.filter(latitude__lte=startLoc.latitude, 
                latitude__gte=endLoc.latitude, 
                longitude__lte=startLoc.latitude,
                longitude__gte=endLoc.longitude)
        elif startLoc.latitude > 0 and startLoc.longitude < 0:
            existingLocations = self.filter(latitude__gte=startLoc.latitude, 
                latitude__lte=endLoc.latitude, 
                longitude__lte=startLoc.latitude,
                longitude__gte=endLoc.longitude)
        elif startLoc.latitude < 0 and startLoc.longitude > 0:
            existingLocations = self.filter(latitude__lte=startLoc.latitude, 
                latitude__gte=endLoc.latitude, 
                longitude__gte=startLoc.latitude,
                longitude__lte=endLoc.longitude)
        else:
            existingLocations = self.filter(latitude__gte=startLoc.latitude, 
                latitude__lte=endLoc.latitude, 
                longitude__gte=startLoc.latitude,
                longitude__lte=endLoc.longitude)

        return existingLocations


    def random_locations(self, startLoc, endLoc, numLocationsToGenerate):
        """
        Give me some random locations inside the rect defined by startLoc and endLoc.
        Make sure the point is on a road! 
        WARNING: Requires external net request (talks to google API)
        This will attempt to make a number of roads equal to the number passed in, but is not guaranteed.
        """
        locPairs = []

        #first let's see if we have some points already inside this square, and we don't need to generate more.
        
        existing = self.existing_locations(startLoc, endLoc)
        # print "found some locations", existing.count()
        if existing.count() > numLocationsToGenerate:
            locs = [ existing[i] for i in sorted(random.sample(xrange(len(existing)), numLocationsToGenerate)) ]
            # print "found some locations, won't generate", locs
            return locs

        for x in range(numLocationsToGenerate):
            lat = random.uniform(float(startLoc.latitude), float(endLoc.latitude))
            lon = random.uniform(float(startLoc.longitude), float(endLoc.longitude))
            locPairs.append((lat, lon))

        on_roads = Location.points_to_roads(locPairs)

        locations = []
        already_seen = []
        for point in on_roads:
            #don't try to make the same thing more than once, gmaps comes back with lots of dupes.
            if point["originalIndex"] in already_seen:
                continue

            already_seen.append(point["originalIndex"])
            newLat = Location.trunc(point["location"]["latitude"], 6)
            newLon = Location.trunc(point["location"]["longitude"], 6)
            newLoc, created = self.get_or_create(latitude=newLat, longitude=newLon, defaults={"latitude": newLat, "longitude": newLon})
            locations.append(newLoc)

        return locations


class Location(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    objects = LocationManager()

    def __unicode__(self):
        return "id: %s lat: %s lon: %s" % (self.pk, self.latitude, self.longitude)

    @staticmethod
    def snap_to_grid(point):
        #Chops off at hundredths (.01)
        return Location.trunc(point, 2)

    @staticmethod
    def next_grid_point(point):
        #Sequentially the next grid point for a point, used when finding top right corner of a grid space.
        #TODO, this won't work at the upper boundaries of lat and lon...
        if point < 0:
            return Location.trunc(float(point) - .01, 2)
        else:
            return Location.trunc(float(point) + .01, 2)

    @staticmethod
    def trunc(num, digits):
        sp = str(num).split('.')
        return float('.'.join((sp[0], sp[1][:digits])))

    @staticmethod
    def points_to_roads(points):
        """
        Points should be a list formatted like 
        ["45.460627,-122.693437", "45.460907,-122.700917"] or 
        [(40.714224, -73.961452), (41.714224, -72.961452)]
        """
        return gmaps.nearest_roads(points)


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
    map_level = models.PositiveSmallIntegerField(default=1, help_text="Current location of the game object. Necessary if a map wasn't already associated with this object, one is created based on this.")
    display_char = models.CharField(max_length=1)

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
        self.game_map = GameMap.objects.map_for_location(self.location, self.map_level)
        self.save()
