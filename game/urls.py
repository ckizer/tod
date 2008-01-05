from django.conf.urls.defaults import *

from tod.game.models import Game
urlpatterns = patterns('tod.game.views',
    (r'^play/$', 'play'),
    (r'^game_over/$', 'game_over'),
    (r'^(?P<game_id>\d+)/select_prompts/$', 'select_prompts'),
)

urlpatterns += patterns ('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Game.objects.all(),'allow_empty': True}),
    (r'^create/$', 'django.views.generic.create_update.create_object', {'model': Game, 'post_save_redirect': '/game/'}),
    (r'^(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', {'model': Game, 'post_delete_redirect': '/game/'}),
)
