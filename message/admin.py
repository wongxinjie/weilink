#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Message, Atuser, Collection, Comment, Picture, Agree, Retweet, MessagePicture
 
class MessageAdmin(admin.ModelAdmin):
	list_display = ['author', 'message_type', 'isoriginal', 'private', 'content', 'publish_time', 'collect_count', 'comment_count', 'retweet_count', 'agree_count', 'read_count']
	

class AtuserAdmin(admin.ModelAdmin):
	list_display = ['attype', 'objectid', 'atuserid', 'useratid', 'attime', 'benoticed']
	
class CollectionAdmin(admin.ModelAdmin):
	list_display = ['userid', 'messageid', 'collect_time']

class AgreeAdmin(admin.ModelAdmin):
	list_display = ['userid', 'authorid', 'messageid', 'benoticed', 'agree_time']
	
class CommentAdmin(admin.ModelAdmin):
	list_display = ['userid', 'authorid', 'messageid', 'content', 'been_read', 'visible_status', 'comment_time']

class PictureAdmin(admin.ModelAdmin):
	list_display = ['userid', 'picture_name', 'picture_path', 'visible_status', 'add_time']

class RetweetAdmin(admin.ModelAdmin):
	list_display = ['originalid', 'retweetmsgid']

class MessagePictureAdmin(admin.ModelAdmin):
	list_display=['pictureid', 'messageid']

admin.site.register(Message, MessageAdmin)
admin.site.register(Atuser, AtuserAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Agree, AgreeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Retweet, RetweetAdmin)
admin.site.register(MessagePicture, MessagePictureAdmin)


	 
