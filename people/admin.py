#-*- coding: utf-8 -*-
from django.contrib import admin
from models import People, Relationship, Blacklist

class PeopleAdmin(admin.ModelAdmin):
	list_display = ['nickname', 'verify_name', 'realname', 'address', 'gender', 'sexual', 'feeling', 'birthday', 'avatar', 'blogurl', 'domainurl', 'introduction', 'contact_email', 'QQ', 'wechat', 'profession', 'label']

class RelationshipAdmin(admin.ModelAdmin):
	list_display = ['wluserid', 'followerid', 'create_time', 'groupid']

class BlacklistAdmin(admin.ModelAdmin):
	list_display = ['wluserid', 'blackerid', 'create_time']
	

	

admin.site.register(People, PeopleAdmin)
admin.site.register(RelationShip, RelationshipAdmin)
admin.site.register(Blacklist, BlacklistAdmin)

