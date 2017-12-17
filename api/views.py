from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from players.serializers import PlayerSerializer
from monsters.serializers import MonsterSerializer
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
        player = user.players.all()[0]

        #update the location for the actor.
        newLoc, created = Location.objects.get_or_create(latitude=lat, longitude=lon, defaults={"latitude": lat, "longitude": lon})
        player.update_location(newLoc)

        #get a game_map for the area.
        gm = player.game_map
        gm.populate()

        data = {}
        data['player'] = PlayerSerializer(player).data
        data['monsters'] = MonsterSerializer(gm.monster_set, many=True).data
        data['items'] = []

        return Response(data)
