from django.conf.urls.defaults import *
from tod.settings import MEDIA_ROOT

urlpatterns = patterns('django.views.generic.simple',
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
)

urlpatterns += patterns('',
    (r"^$", "tod.views.index"),
    (r"^test/$", "tod.views.test"),
    (r"^accounts/login/$", "django.contrib.auth.views.login"),
    (r"^accounts/register/$", "tod.views.register"),
    (r"^accounts/logout/$", "tod.views.logout_view"),
    (r"^mockups/$", "tod.views.mockups"),
    (r"^prompt/", include("tod.prompt.urls")),
    (r"^game/", include ("tod.game.urls")),
    (r"^player/", include ("tod.player.urls")),
    (r"^comment/", include ("tod.comment.urls")),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
