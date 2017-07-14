from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.browse_games, {'owned_only': False}, name='browse_games'),
    url(r'^games/(?P<game_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^games/(?P<game_id>[0-9]+)/buy/$', views.buy_game, name='buy_game'),
    url(r'^games/(?P<game_id>[0-9]+)/payment/$', views.payment, name='payment'),
    url(r'^games/(?P<game_id>[0-9]+)/message/$', views.message, name='message'),
    url(r'^my_games/$', login_required(views.browse_games), {'owned_only': True}, name='my_games'),
    url(r'^add_game/$', views.add_game, name='add_game'),
    url(r'^edit_game/(?P<game_id>[0-9]+)/$', views.edit_game, name='edit_game'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^developer_profile/$', views.developer_profile, name='developer_profile'),
    url(r'^remove_game/(?P<game_id>[0-9]+)/$', views.remove_game, name='remove_game')
]
