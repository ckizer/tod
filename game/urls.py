from django.conf.urls.defaults import *

from viking.story.models import Story
urlpatterns = patterns('viking.story.views',
    (r'^(?P<story_id>\d+)/story/$', 'story'),
)

urlpatterns += patterns ('',
    (r'^$', 'django.views.generic.list_detail.object_list', {'queryset': Story.objects.all(),'allow_empty': True}),
)
