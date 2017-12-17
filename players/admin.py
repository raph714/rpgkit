from django.contrib import admin
from players.models import Player, Race, Class, PlayerMessage

admin.site.register(Player)
admin.site.register(Race)
admin.site.register(Class)
admin.site.register(PlayerMessage)
