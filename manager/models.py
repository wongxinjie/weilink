#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Manager(models.Model):
	user = models.OneToOneField(User, verbose_name=u'用户')
	name = models.CharField(max_length=50, unique=True, verbose_name=u'昵称')
	permission = models.IntegerField(default=0, verbose_name=u'权限')
	
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'管理员'
	
	
