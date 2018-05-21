from django.conf.urls import url
from api import views


urlpatterns = [
	#post values for 'username' and 'password' to this endpoint to get a token.
	url(r'^game_state/', views.GameState.as_view(), name='GameState'),
	url(r'^action/', views.Action.as_view(), name='Action'),
	# url(r'^create_character/', views.GameState.as_view(), name='GameState'),
]