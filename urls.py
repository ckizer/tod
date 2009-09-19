from django.conf.urls.defaults import *
from django.contrib import admin
from tod.settings import MEDIA_ROOT

admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
    (r'^terms/$', 'direct_to_template', {'template': 'termsofuse.html'}),
)

urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)$', admin.site.root),
    (r"^$", "tod.views.index"),
    (r"^test/$", "tod.views.test"),
    (r"^accounts/login/$", "django.contrib.auth.views.login"),
    (r"^accounts/register/$", "tod.common.views.register"),
    (r"^accounts/logout/$", "tod.views.logout_view"),
    (r"^mockups/$", "tod.views.mockups"),
    (r"^prompt/", include("tod.prompt.urls")),
    (r"^game/", include ("tod.game.urls")),
    (r"^player/", include ("tod.player.urls")),
    (r"^comment/", include ("tod.comment.urls")),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
