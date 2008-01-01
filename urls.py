from django.conf.urls.defaults import *
from tod.settings import MEDIA_ROOT

urlpatterns = patterns('django.views.generic.simple',
    (r'^$', 'direct_to_template', {'template': 'home.html'}),
)

urlpatterns += patterns('',
    (r"^test/$", "tod.views.test"),
    (r"^prompt/", include("tod.prompt.urls")),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}),
)
