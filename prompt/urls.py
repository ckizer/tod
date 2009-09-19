from django.conf.urls.defaults import *
from tod.prompt.models import Prompt

urlpatterns = patterns('tod.prompt.views', 
    (r'^$', 'index'),
    (r'^create/$', 'detail'),
    (r'^(?P<object_id>\d+)/delete/$', 'limited_delete_object', {'model': Prompt, 'post_delete_redirect': '/prompt/'}),
)

