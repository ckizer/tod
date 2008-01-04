from django.conf.urls.defaults import *

from tod.game.models import Game
urlpatterns = patterns('tod.game.views',
    (r'^play/$', 'play'),
)

urlpatterns += patterns ('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Game.objects.all(),}),
    (r'^create/$', 'django.views.generic.create_update.create_object', {'model': Game, 'post_save_redirect': '/game/'}),
    (r'^(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', {'model': Game, 'post_delete_redirect': '/game/'}),
)
