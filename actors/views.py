from django.contrib.auth.models import User
from actors.models import Actor, Race, ActorClass
from actors.serializers import ActorSerializer
from rpgkit.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets, generics, permissions, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


class ActorViewSet(viewsets.ModelViewSet):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'actors': reverse('actor_list', request=request, format=format)
    })


@api_view(['GET'])
def roll_stats(request, format=None):
    a = Actor()
    rolls = a.roll_stats()
    return Response(rolls)


@api_view(['GET'])
def list_races(request, format=None):
    return Response([{"id": race.id, "name": race.name, "description": race.description} for race in Race.objects.all()])


@api_view(['GET'])
def list_classes(request, format=None):
    return Response([{"id": obj.id, "name": obj.name, "description": obj.description} for obj in ActorClass.objects.all()])


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
        actorClass = ActorClass.objects.get(id = int(postArgs["class"]))

        newActor = Actor(base_strength = int(postArgs["str"]),
                        base_dexterity = int(postArgs["dex"]),
                        base_constitution = int(postArgs["con"]),
                        base_intelligence = int(postArgs["int"]),
                        base_wisdom = int(postArgs["wis"]),
                        base_charisma = int(postArgs["cha"]),
                        race = race,
                        actor_class = actorClass,
                        owner = request.user
                    )

        newActor.save()

        return Response({"ok": True})

