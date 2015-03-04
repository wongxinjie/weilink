#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('people.views', 
	url(r'^home/$', 'home', name='home'),
	url(r'^profile/(?P<pid>(\d+))/$', 'profile', name='profile'),
	url(r'^fillinfo/$', 'fillinfo', name='fillinfo'),
	url(r'^set/$', 'set_info', name='set_info'),
	url(r'^follow/$', 'follow_page', name='follow_page'),
	url(r'^fan/$', 'fan_page', name='fan_page'),
	url(r'^add_follow', 'add_follow', name='add_follow'),
	url(r'^remove_follow', 'remove_follow', name='remove_follow'),
	url(r'^remove_fan', 'remove_fan', name='remove_fan'),
	url(r'^add_blacklist', 'add_blacklist', name='add_blacklist'),
	url(r'^remove_blacklist', 'remove_blacklist', name='remove_blacklist'),
)

