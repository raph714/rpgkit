from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from base.models import Base, Location
import googlemaps
import datetime
from game_controller.models import GameController
import random
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)


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
        loc = Location.objects.map_origin_point(location)

        aMap, created = self.get_or_create(
            origin_location=loc,
            level=level, 
            defaults={"origin_location": loc, "level": level})

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

    def populate(self):
        """
        Figure out what is in the map
        """
        #get the game controller
        gc = GameController.objects.all()[0]

        now = timezone.now()

        # if now > self.populate_date + datetime.timedelta(minutes=gc.monster_spawn_delay):
        #get a number between .5 and 1.5
        seed = random.random() + .5

        #multiply by the average num to get the number we're going to make moew
        num_monsters = int(gc.monster_density * seed)

        #figure out how many monsters are on the map right now... and how many we need to make.
        monster_count = self.monster_set.count()

        if monster_count < num_monsters:
            from monsters.models import MonsterType
            #get some monsters that might show up on this dungeon level.
            monsters = MonsterType.objects.filter(min_dungeon_level__lte=self.level, max_dungeon_level__gte=self.level)
            num_to_add = num_monsters - monster_count
            map_top_corner = Location.objects.map_top_right_point(self.origin_location)

            #number of locs is probably not going to be equal to the amount we wanted when we passed in
            #because google only gives us back points that were already close to a road.
            locs = Location.objects.random_locations(self.origin_location, map_top_corner, num_to_add)

            for loc in locs:
                #TODO deal with monster rarity.
                index = random.randint(0, monsters.count()-1)
                aMonster = monsters[index]
                aMonster.generate(self, loc)
