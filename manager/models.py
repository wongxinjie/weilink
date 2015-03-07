#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Manager(models.Model):
	user = models.OneToOneField(User, verbose_name=u'用户')
	name = models.CharField(max_length=50, unique=True, verbose_name=u'昵称')
	permission = models.IntegerField(default=0, verbose_name=u'权限')
	contact_email = models.EmailField(unique=True, verbose_name=u'联系邮箱')
	create_time = models.DatetimeField(auto_now_add=True, verbose_name=u'创建时间')
	
	
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['create_time']
		verbose_name_plural = verbose_name = u'管理员'
	
	
