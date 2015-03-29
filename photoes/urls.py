#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('photoes.views',
	url(r'^upload_avatar/$', 'upload_avatar', name='upload_avatar'),
)
