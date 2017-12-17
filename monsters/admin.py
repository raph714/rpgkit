from django.contrib import admin
from monsters.models import Monster, MonsterType

# Register your models here.
admin.site.register(Monster)
admin.site.register(MonsterType)