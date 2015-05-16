#-*- coding: utf-8 -*-
from django.contrib import admin
from models import People, Relationship, Blacklist, Whitelist, Reputation

class PeopleAdmin(admin.ModelAdmin):
	list_display = ['nickname', 'verify_status', 'realname', 'address', 'gender', 'sexual', 'feeling', 'birthday', 'avatar', 'blogurl', 'domainurl', 'introduction', 'contact_email', 'QQ', 'wechat', 'profession', 'label']

class RelationshipAdmin(admin.ModelAdmin):
	list_display = ['wluserid', 'followerid', 'create_time', 'benoticed', 'groupid']

class BlacklistAdmin(admin.ModelAdmin):
	list_display = ['wluserid', 'blackerid', 'create_time']

class WhitelistAdmin(admin.ModelAdmin):
	list_display = ['wluser', 'white_list']
	
class ReputationAdmin(admin.ModelAdmin):
	list_display = ['wlpeople', 'score', 'level', 'location']
	

admin.site.register(People, PeopleAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(Blacklist, BlacklistAdmin)
admin.site.register(Whitelist, WhitelistAdmin)
admin.site.register(Reputation, ReputationAdmin)

