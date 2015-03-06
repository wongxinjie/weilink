#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('message.views',
	url(r'^message/(?P<mid>(\d+))/$', 'show_message', name='show_message'),
	url(r'^collecions/$', 'collections', name='show_collection'),
	url(r'^atmessage/$', 'atmessage', name='atmessage'),
	url(r'^atcomment/$', 'atcomment', name='atcomment'),
	url(r'^get_comment_list/$', 'get_comment_list', name='get_comment_list'),
	url(r'^get_retweet_list/$', 'get_retweet_list', name='get_retweet_list'),
	url(r'^get_agree_list/$', 'get_agree_list', name='get_agree_list'),
	url(r'^post_message/$', 'post_message', name='post_message'),
	url(r'^remove_message/$', 'remove_message', name='remove_message'),
	url(r'^post_comment/$', 'post_comment', name='post_comment'),
	url(r'^remove_comment/$', 'remove_comment', name='remove_comment'),
	url(r'^retweet/$', 'retweet', name='retweet'),
	url(r'^add_collection', 'add_collection', name='add_collection'),
	url(r'^remove_collection', 'remove_collection', name='remove_collection'),	
	url(r'^agree/$', 'agree', name='agree'),
)

