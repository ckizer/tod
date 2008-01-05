from django.conf.urls.defaults import *
from tod.prompt.models import Prompt
urlpatterns = patterns('tod.prompt.views', 
    (r'^$', 'index'),
    (r'^(?P<prompt_id>\d+)/complete/$', 'complete'),
)

urlpatterns += patterns('',
    (r'^list/$', 'django.views.generic.list_detail.object_list',  {'queryset': Prompt.objects.all(),}),
    (r'^create/$', 'django.views.generic.create_update.create_object', {'model': Prompt, 'post_save_redirect': '/prompt/list/'}),
    (r'^(?P<object_id>\d+)/delete/$', 'django.views.generic.create_update.delete_object', {'model': Prompt, 'post_delete_redirect': '/prompt/list/'}),
)
