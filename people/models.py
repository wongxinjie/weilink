#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class People(models.Model):
	GENDER_CHOICES = (
		(u'M', u'男'),
		(u'F', u'女'),
		(u'U', u'保密'),
	)
	SEXUAL_CHOICES = (
		(u'S', u'异性恋'),
		(u'H', u'同性恋'),
		(u'B', u'双性恋'),
		(u'U', u'保密'),
	)
	FEELING_CHOICES =  (
		(u'S', u'单身'),
		(u'A', u'暧昧'),
		(u'I', u'恋爱中'),
		(u'E', u'订婚'),
		(u'D', u'离婚'),
		(u'U', u'保密'),
	)
	user = models.OneToOneField(User)
	nickname=models.CharField(max_length=60, unique=True, verbose_name=u'昵称')
	verify_status = models.IntegerField(default=0, verbose_name=u'验证状态')
	realname = models.CharField(max_length=40, blank=True, verbose_name=u'真实姓名')
	address = models.CharField(max_length=120, blank=True, verbose_name=u'地址')
	gender = models.CharField(max_length=4, choices=GENDER_CHOICES, verbose_name='性别')
	sexual = models.CharField(max_length=4, choices=SEXUAL_CHOICES, verbose_name=u'性取向')
	feeling = models.CharField(max_length=4, choices=FEELING_CHOICES, verbose_name=u'感情状况')
	birthday = models.DateField(blank=True, verbose_name=u'出生日期')
	avatar = models.CharField(max_length=200, default='', verbose_name=u'头像')
	blogurl = models.CharField(max_length=200, blank=True, verbose_name=u'博客地址')
	domainurl = models.CharField(max_length=50, unique=True, verbose_name=u'个性域名')
	introduction = models.CharField(max_length=400, blank=True, verbose_name=u'简介')
	contact_email = models.EmailField(blank=True, verbose_name=u'邮箱')
	QQ = models.CharField(max_length=20, blank=True,  verbose_name=u'QQ')
	wechat = models.CharField(max_length=20, blank=True, verbose_name=u'微信')
	profession = models.CharField(max_length=20, blank=True, verbose_name=u'职业')
	label = models.CharField(max_length=200,blank=True, verbose_name=u'标签')
	
	def __unicode__(self):
		return self.nickname
	
	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'用户信息'


class Relationship(models.Model):
	wluserid = models.IntegerField(verbose_name=u'被关注者')
	followerid = models.IntegerField(verbose_name=u'关注者')	
	create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')
	groupid = models.IntegerField(default=0, verbose_name=u'分组')

	def __unicode__(self):
		return str(followerid)+'follow'+str(wluserid)

	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'关系'
	

class Blacklist(models.Model):
	wluserid = models.IntegerField(verbose_name=u'用户')
	blackerid = models.IntegerField(verbose_name=u'被拉黑用户')
	create_time = models.DateTimeField(verbose_name=u'添加时间')
	
	def __unicode__(self):
		return str(wluserid)+'add'+str(blackerid)+'to blacklist'

	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'黑名单'
	
	
	

