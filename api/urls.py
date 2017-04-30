from django.conf.urls import url
from rest_framework.authtoken import views as tokenViews
from api import views


urlpatterns = [
	#post values for 'username' and 'password' to this endpoing to get a token.
    url(r'^token/', tokenViews.obtain_auth_token),
	url(r'^game_state/', views.GameState.as_view(), name='GameState'),
]