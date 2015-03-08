#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('manager.views',
	url(r'^login/$', 'manager_login', name='manager_login'),
	url(r'^create/$', 'create_manager', name='create_manager'),
	url(r'^mlist/$', 'list_manager', name='list_manager'),
	url(r'^ulist/$', 'list_user', name='list_user'),
	url(r'^banduser/$', 'band_user', name='band_user'),
	url(r'^bandmanager/$', 'band_manager', name='band_manager'),
	url(r'^remove/manager/(?P<mid>(\d+))/$', 'remove_manager', name='remove_manager'),
)


