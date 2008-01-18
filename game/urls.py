from django.conf.urls.defaults import *

from tod.game.models import Game
urlpatterns = patterns('tod.game.views',
    (r'^(?P<game_id>\d+)/play/$', 'play'),
    (r'^(?P<game_id>\d+)/game_over/$', 'game_over'),
    (r'^(?P<game_id>\d+)/complete/$', 'complete'),
    (r'^(?P<game_id>\d+)/wimp_out/$', 'wimp_out'),
    (r'^(?P<game_id>\d+)/begin_game/$', 'begin_game'),  
    (r'^(?P<game_id>\d+)/$', 'detail'),
    (r'^(?P<game_id>\d+)/players_added/$', 'players_added'),
    (r'^(?P<game_id>\d+)/select_prompts/$', 'select_prompts'),
)

urlpatterns += patterns ('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Game.objects.all(),'allow_empty': True}),
    (r'^create/$', 'django.views.generic.create_update.create_object', {'model': Game}),
    (r'^(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', {'model': Game, 'post_delete_redirect': '/game/'}),
)
