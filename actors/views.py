from django.contrib.auth.models import User
from actors.models import Actor
from actors.serializers import ActorSerializer
from rpgkit.permissions import IsOwnerOrReadOnly
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse


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