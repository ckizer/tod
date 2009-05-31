from django.conf.urls.defaults import *

from tod.game.models import Game
urlpatterns = patterns('tod.game.views',
#display objects
    (r'^$', 'object_list'),
    (r'^(?P<game_id>\d+)/$', 'detail'),
#create process
    (r'^create/$', 'create_object'),
    (r'^quickstart/$', 'quickstart'),
    (r'^(?P<game_id>\d+)/players_added/$', 'players_added'),
    (r'^(?P<game_id>\d+)/select_prompts/$', 'select_prompts'),
#gameplay flow
    (r'^(?P<game_id>\d+)/begin_game/$', 'begin_game'),  
    (r'^(?P<game_id>\d+)/choice/$', 'choice'),
    (r'^(?P<game_id>\d+)/play/(?P<choice>(truth|dare))/$', 'play'),
    (r'^(?P<game_id>\d+)/complete/$', 'complete'),
    (r'^(?P<game_id>\d+)/wimp_out/$', 'wimp_out'),
    (r'^(?P<game_id>\d+)/game_over/$', 'game_over'),
#delete process
    (r'^(?P<object_id>\d+)/delete/$', 'limited_delete_object', {'model': Game, 'post_delete_redirect': '/game/'}),
)

