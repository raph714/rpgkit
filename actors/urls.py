from django.conf.urls import url, include
from actors import views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'actors', views.ActorViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^roll_stats/', views.roll_stats),
]
