from django.conf.urls.defaults import *

from tod.game.models import Game
urlpatterns = patterns('tod.game.views',
    (r'^(?P<game_id>\d+)/play/(?P<choice>(truth|dare))/$', 'play'),
    (r'^(?P<game_id>\d+)/choice/$', 'choice'),
    (r'^(?P<game_id>\d+)/game_over/$', 'game_over'),
    (r'^(?P<game_id>\d+)/complete/$', 'complete'),
    (r'^(?P<game_id>\d+)/wimp_out/$', 'wimp_out'),
    (r'^(?P<game_id>\d+)/begin_game/$', 'begin_game'),  
    (r'^(?P<game_id>\d+)/$', 'detail'),
    (r'^(?P<game_id>\d+)/players_added/$', 'players_added'),
    (r'^(?P<game_id>\d+)/select_prompts/$', 'select_prompts'),
    (r'^$', 'object_list'),
    (r'^create/$', 'create_object'),
    (r'^(?P<object_id>\d+)/delete/$', 'limited_delete_object', {'model': Game, 'post_delete_redirect': '/game/'}),
)

