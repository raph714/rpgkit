from django.contrib.auth.models import User
from players.models import Player, Race, Class
from players.serializers import PlayerSerializer
from actors.models import Actor
from rpgkit.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, generics, permissions, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class PlayerViewSet(viewsets.ModelViewSet):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'actors': reverse('actor_list', request=request, format=format)
    })


@api_view(['GET'])
def roll_stats(request, format=None):
    p = Player()
    rolls = p.roll_stats()
    return Response(rolls)


@api_view(['GET'])
def list_races(request, format=None):
    return Response([{"id": race.id, "name": race.name, "description": race.description} for race in Race.objects.all()])


@api_view(['GET'])
def list_classes(request, format=None):
    return Response([{"id": obj.id, "name": obj.name, "description": obj.description} for obj in Class.objects.all()])


class CreateActor(APIView):
    """
    Makes an actor and associates it with the current user.

    * Requires token authentication.
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        postArgs = request.POST

        race = Race.objects.get(id = int(postArgs["race"]))
        actorClass = Class.objects.get(id = int(postArgs["class"]))

        #TODO Store rolls and use the last one rather than accepting any input, in case there are cheaters...
        newPlayer = Player(base_strength = int(postArgs["str"]),
                        base_dexterity = int(postArgs["dex"]),
                        base_constitution = int(postArgs["con"]),
                        base_intelligence = int(postArgs["int"]),
                        base_wisdom = int(postArgs["wis"]),
                        base_charisma = int(postArgs["cha"]),
                        race = race,
                        actor_class = actorClass,
                        owner = request.user
                    )

        newPlayer.save()

        return Response({"ok": True})

