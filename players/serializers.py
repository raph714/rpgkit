from rest_framework import serializers
from players.models import Player
from base.serializers import LocationSerializer


class PlayerSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    location = LocationSerializer()
    
    class Meta:
        model = Player
        fields = '__all__'
