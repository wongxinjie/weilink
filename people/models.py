#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class WlSettings(models.Model):
	MODE_CHOICES = (
		('A', 'ALL'),
		('S', 'SOME'),
		('N', 'NONE'),
	)
	wluser = models.OneToOneField(User)
	background = models.IntegerField(default=0, verbose_name=u'背景设置')
	account_mode = models.CharField(max_length=4, choices=MODE_CHOICES, default='A', verbose_name=u'帐号模式')
	account_visible = models.BooleanField(default=True, verbose_name=u'帐号可搜到')
	tweet_visible = models.BooleanField(default=True, verbose_name=u'推可搜到')
	message_remind = models.BooleanField(default=True, verbose_name=u'消息提醒')

	def __unicode__(self):
		return 'user'+str(self.wluser.id)+'settings'

	class Meta:
		verbose_name_plural = verbose_name = u'设置'


class People(models.Model):
	GENDER_CHOICES = (
		(u'M', u'男'),
		(u'F', u'女'),
		(u'B', u'人妖'),
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
		(u'M', u'已婚'),
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
	birthday = models.DateField(auto_now_add=True, verbose_name=u'出生日期')
	avatar = models.CharField(max_length=200, default='', verbose_name=u'头像')
	blogurl = models.CharField(max_length=200, blank=True, verbose_name=u'博客地址')
	domainurl = models.CharField(max_length=50, blank=True, verbose_name=u'个性域名')
	introduction = models.CharField(max_length=400, blank=True, verbose_name=u'简介')
	contact_email = models.EmailField(blank=True, verbose_name=u'邮箱')
	QQ = models.CharField(max_length=20, blank=True,  verbose_name=u'QQ')
	wechat = models.CharField(max_length=20, blank=True, verbose_name=u'微信')
	profession = models.CharField(max_length=20, blank=True, verbose_name=u'职业')
	label = models.CharField(max_length=200,blank=True, verbose_name=u'标签')
	
	def __unicode__(self):
		return self.nickname

	def get_wlsettings(self):
		return self.user.wlsettings
	
	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'用户信息'


class Relationship(models.Model):
	wluserid = models.IntegerField(verbose_name=u'被关注者')
	followerid = models.IntegerField(verbose_name=u'关注者')	
	create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')
	benoticed = models.BooleanField(default=False, verbose_name=u'新粉丝提醒')
	groupid = models.IntegerField(default=0, verbose_name=u'分组')

	def __unicode__(self):
		return str(self.followerid)+'follow'+str(self.wluserid)

	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'关系'
	

class Blacklist(models.Model):
	wluserid = models.IntegerField(verbose_name=u'用户')
	blackerid = models.IntegerField(verbose_name=u'被拉黑用户')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')
	
	def __unicode__(self):
		return str(self.wluserid)+'add'+str(self.blackerid)+'to blacklist'

	class Meta:
		ordering = ['id']
		verbose_name_plural = verbose_name = u'黑名单'




class Whitelist(models.Model):
	wluser = models.OneToOneField(User)
	white_list = models.CharField(max_length=200, verbose_name=u'')

	def __unicode__(self):
		return 'user'+str(self.wluser.id)+'whitelist'

	def get_whitelist(self):
		return self.white_list

	class Meta:
		verbose_name_plural = verbose_name = u'白名单'


class PasswordTicket(models.Model):
	wluserid = models.IntegerField(verbose_name=u'用户ID')
	access_token = models.CharField(max_length=100, verbose_name=u'access_token')
	create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'生成时间')



class Reputation(models.Model):
	wlpeople = models.OneToOneField(People)
	score = models.IntegerField(default=0, verbose_name=u'积分')
	level = models.IntegerField(default=0, verbose_name=u'等级')
	location = models.CharField(max_length=50, verbose_name=u'登录地址')

	
	
	

