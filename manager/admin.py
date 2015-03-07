#-*- coding: utf-8 -*-
from django.contrib import admin
from models import Manager

class ManagerAdmin(admin.ModelAdmin):
	list_display = ['user', 'name', 'permission', 'contact_email', 'create_time']
	
admin.site.register(Manager, ManagerAdmin)


