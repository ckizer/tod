from django.conf.urls.defaults import *
from tod.prompt.models import Prompt
urlpatterns = patterns('tod.prompt.views', 
    (r'^(?P<prompt_id>\d+)/complete/$', 'complete'),
    (r'^create/$', 'detail'),
)

urlpatterns += patterns('',
    (r'^$', 'django.views.generic.list_detail.object_list',  {'queryset': Prompt.objects.all(),}),
    (r'^(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', {'model': Prompt, 'post_delete_redirect': '/prompt/'}),
)
