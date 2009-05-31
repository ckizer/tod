from django.conf.urls.defaults import *

from tod.player.models import Player

urlpatterns = patterns('tod.player.views',
    (r'^play/$', 'play'),
    (r'^(?P<game_id>\d+)/create/$','create'),
    (r'^(?P<player_id>\d+)/delete/$','delete'),
)

urlpatterns += patterns('django.views.generic.simple',
                        ('^(?P<id>\d+)/$', 'redirect_to', {'url': '/player/%(id)s/create/'}),
)



