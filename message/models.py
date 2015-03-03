#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
	author = models.ForeignKey(User, verbose_name=u'用户')
	message_type = models.IntegerField(default=0, verbose_name=u'微博类型')
	private = models.BooleanField(default=False, verbose_name=u'自己可见')
	content = models.CharField(max_length=280, verbose_name=u'微博内容')
	publish_time = models.DateTimeField(auto_now_add=True, verbose_name=u'发布时间')
	collect_count = models.IntegerField(default=0, verbose_name=u'收藏次数')
	comment_count = models.IntegerField(default=0, verbose_name=u'评论次数')
	retweet_count = models.IntegerField(default=0, verbose_name=u'转发次数')
	agree_count = models.IntegerField(default=0, verbose_name=u'赞次数')
	read_count = models.IntegerField(default=0, verbose_name=u'阅读次数')
	label = models.CharField(max_length=80, blank=True, verbose_name=u'标签')
	picture_id = models.IntegerField(blank=True, verbose_name=u'图片ID')
	
	def __unicode__(self):
		return self.content
	
	class Meta:
		ordering=['publish_time']
		verbose_name_plural = verbose_name = u'微博'

class Atuser(models.Model):
	ATTYPE_CHOICES = (
		(u'M', u'message'), 
		(u'C', u'comment'), 
	)

	attype = models.CharField(max_length=4, choices=ATTYPE_CHOICES, verbose_name=u'类型')
	messageid = models.IntegerField(blank=True, verbose_name=u'微博ID')
	commentid = models.IntegerField(blank=True, verbose_name=u'评论ID')
	atuserid = models.IntegerField(verbose_name=u'AT用户')
	useratid = models.IntegerField(verbose_name=u'被AT用户')
	attime = models.DateTimeField(auto_now_add=True, verbose_name=u'AT时间')

	
	def __unicode__(self):
		return str(self.atuserid)+'@'+str(self.useratid)
	
	class Meta:
		ordering = ['attime']
		verbose_name_plural = verbose_name=u'AT'


class Collection(models.Model):
	userid = models.IntegerField(verbose_name=u'收藏用户ID')
	messageid = models.IntegerField(verbose_name=u'微博ID')
	collect_time = models.DateTimeField(auto_now_add=True, verbose_name=u'收藏时间')
	
	def __unicode__(self):
		return str(userid)+':'+str(messageid)
	
	class Meta:
		ordering = ['collect_time']
		verbose_name_plural = verbose_name = u'收藏'

class Comment(models.Model):
	userid = models.IntegerField(verbose_name=u'评论用户')
	messageid = models.IntegerField(verbose_name=u'微博ID')
	content = models.CharField(max_length=280, verbose_name=u'评论内容')
	been_read = models.BooleanField(default=False, verbose_name=u'阅读状态')
	visible_status = models.IntegerField(default=0, verbose_name=u'可见状态')
	comment_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')
	
	def __unicode__(self):
		return self.content
	
	class Meta:
		ordering = ['comment_time']
		verbose_name_plural = verbose_name=u'评论'
	

class Picture(models.Model):
	userid = models.IntegerField(verbose_name=u'用户ID')
	picture_name = models.CharField(max_length=100, verbose_name=u'图片名')
	visible_status = models.IntegerField(default=0, verbose_name=u'可见状态')
	add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

	def __unicode__(self):
		return self.picture_name
	
	def get_picture_url(self):
		url = '/static/images/%s' % self.picture_name
		return url
	
	class Meta:
		ordering = ['add_time']
		verbose_name_plural = verbose_name=u'图片'
		


