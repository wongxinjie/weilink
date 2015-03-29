#-*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('reminder.views',
	url(r'^get_reminder/$', 'get_reminder', name='get_reminder'),
	url(r'^message_at', 'message_at', name='message_at'),
	url(r'^comment_at', 'comment_at', name='comment_at'),
	url(r'^received_comment', 'received_comment', name='received_comment'),
	url(r'^sended_comment', 'sended_comment', name='sended_comment'),
	url(r'^agree_page', 'agree_page', name='agree_page'),
	url(r'^letter_page', 'letter_page', name='letter_page'),
	url(r'^recent_contact', 'recent_contact', name='recent_contact'),
)


