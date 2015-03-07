#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('letter.views',
	url(r'^send_letter/$', 'send_letter', name='send_letter'),
	url(r'^people/(?P<pid>(\d+))/$', 'history_letter', name='history_letter'),
	url(r'^view/$','letter_page', name='letter_page'),
	url(r'^remove/people/(?P<pid>(\d+))/$', 'remove_letters', name='remove_letter'),
)


