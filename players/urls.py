from django.conf.urls import url, include
from players import views
from rest_framework.routers import DefaultRouter


# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'actors', views.PlayerViewSet)

urlpatterns = [
	url(r'^', include(router.urls)),
	url(r'^roll_stats/', views.roll_stats),
	url(r'^list_races/', views.list_races),
	url(r'^list_classes/', views.list_classes),
	url(r'^create_actor/', views.CreateActor.as_view(), name="create_actor"),
]
