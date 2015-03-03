#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Message, Atuser, Collection, Comment, Picture
 
class MessageAdmin(admin.ModelAdmin):
	list_display = ['author', 'message_type', 'content', 'publish_time', 'collect_count', 'comment_count', 'retweet_count', 'agree_count', 'read_count', 'label', 'picture_id']
	

class AtuserAdmin(admin.ModelAdmin):
	list_display = ['attype', 'messageid', 'commentid', 'atuserid', 'useratid', 'attime']
	
class CollectionAdmin(admin.ModelAdmin):
	list_display = ['userid', 'messageid', 'collect_time']
	
class CommentAdmin(admin.ModelAdmin):
	list_display = ['userid', 'messageid', 'content', 'been_read', 'visible_status', 'comment_time']

class PictureAdmin(admin.ModelAdmin):
	list_display = ['userid', 'picture_name', 'visible_status', 'add_time']

admin.site.register(Message, MessageAdmin)
admin.site.register(Atuser, AtuserAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Picture, PictureAdmin)

	 
