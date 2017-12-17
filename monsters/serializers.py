from rest_framework import serializers
from monsters.models import Monster
from base.serializers import LocationSerializer


class MonsterSerializer(serializers.ModelSerializer):
    location = LocationSerializer()

    class Meta:
        model = Monster
        fields = ('location', 'level', 'hp', 'name', 'description', 'display_char')