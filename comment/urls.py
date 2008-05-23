from django.conf.urls.defaults import *

from tod.comment.models import Comment

urlpatterns = patterns('tod.comment.views',
    (r'^create/$','create'),
    (r'^(?P<comment_id>\d+)/delete/$','delete'),
)


