from django.conf.urls import url
from . import views

app_name = 'post'

urlpatterns = [
    url(r'^list', views.PostList.as_view(), name='lists'),
    
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/'\
    r'(?P<post>[-\w]+)/$', views.detail, name='post_detail'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/'\
    r'(?P<post>[-\w]+)/delete/$', views.delete, name='post_delete'),

    url(r'^create/$', views.post_create, name="post_create"),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/'\
    r'(?P<post>[-\w]+)/update/$', views.post_update, name='post_update'), 

    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),

    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
]
