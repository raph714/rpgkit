from django.contrib import admin
from actors.models import Actor, ActorMessage, Race


admin.site.register(Actor)
admin.site.register(ActorMessage)
admin.site.register(Race)