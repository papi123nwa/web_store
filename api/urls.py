from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^games/$', views.get_games),
    url(r'^games/(?P<game_id>[0-9]+)/$', views.get_game_detail),
]
