from django.conf.urls import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'poll.views.index', name='index'),
    url(r'^vote/(?P<id>\d+)/', 'poll.views.vote', name='vote')
)
