from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from actors.serializers import ActorSerializer
import googlemaps
from datetime import datetime
from game_map.models import GameMap
from base.models import Location

"""
This is responsible for the main game loop and logic.

Take an request from the user, including a location, and an optional action.
Determine if the location is close to the edges of the bounds of the map.
	Expand the map, populate the unpopulated areas with items and monsters.

Determine any appropriate responses to the action.
	Monster attacks, movement, drops if death.

Send back a snippet of code representing an appropriate response.

Full state - entire json response with everything.
Melee Attack - id of target. return response from target and changes in state, message.
Range Attack - id of target, return response from target and changes in state, message.
Magic attack - id of target, spell, returns change in state and any responses.
Position change - new coords, response with changes and message.
wear/weild an item
take off an item
use a staff
cast a spell
"""


class GameState(APIView):
    """
    View returns the state of the world based on a user's location.
    User location is updated.

    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        #get lat and lon out of the request
        lat = request.GET['lat']
        lon = request.GET['lon']

        #figure out who the actor is we're talking about here...
        user = request.user
        actor = user.actors.all()[0]

        #update the location for the actor.
        newLoc = Location(latitude=lat, longitude=lon)
        newLoc.save()
        actor.update_location(newLoc)

        #get a game_map for the area.
        gm = actor.game_map

        gmaps = googlemaps.Client(key='AIzaSyAW-1uN9-jxoiW0v2bP14KC5guXZea7Q3o')

        # # Geocoding an address
        # geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

        # # Look up an address with reverse geocoding
        # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

        # # Request directions via public transit
        # now = datetime.now()
        # directions_result = gmaps.directions("Sydney Town Hall",
        #                                      "Parramatta, NSW",
        #                                      mode="transit",
        #                                      departure_time=now)

        print gmaps.nearest_roads([(40.714224, -73.961452), (41.714224, -72.961452)])

        return Response(ActorSerializer(actor).data)
