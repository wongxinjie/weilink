#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class Message(models.Model):
	author = models.ForeignKey(User, verbose_name=u'用户')
	message_type = models.IntegerField(default=0, verbose_name=u'微博类型')
	isoriginal = models.BooleanField(default=True, verbose_name=u'原创')
	originalid = models.IntegerField(blank=True, verbose_name=u'原创id')
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

	def get_author(self):
		people = self.author.people
		return people
	
	def get_nickname(self):
		people = self.author.people
		return people.nickname
	
	def get_retweet_text(self):
		people = self.author.people
		nickname = people.nickname
		retweet_text = '//@'+nickname+':'+self.content
		return retweet_text
	
	class Meta:
		ordering=['publish_time']
		get_latest_by = 'publish_time'
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
	benoticed = models.BooleanField(default=False, verbose_name=u'已提醒')
	attime = models.DateTimeField(auto_now_add=True, verbose_name=u'AT时间')

	
	def __unicode__(self):
		return str(self.atuserid)+'@'+str(self.useratid)
	
	def get_message(self):
		message = get_object_or_404(Message,  pk=self.messageid)
		return message
	
	def get_atuser(self):
		user = get_object_or_404(User, pk=self.atuserid)
		people = user.people
		return people
	
	class Meta:
		ordering = ['attime']
		verbose_name_plural = verbose_name=u'AT'


class Collection(models.Model):
	userid = models.IntegerField(verbose_name=u'收藏用户ID')
	messageid = models.IntegerField(verbose_name=u'微博ID')
	collect_time = models.DateTimeField(auto_now_add=True, verbose_name=u'收藏时间')
	
	def __unicode__(self):
		return str(self.userid)+':'+str(self.messageid)
	
	def get_message(self):
		message = get_object_or_404(Message, pk=self.messageid)
		return message

	def get_message_author(self):
		message = get_object_or_404(Message, pk=self.messageid)
		user = message.author
		author = user.people
		return author
	
	def get_collector(self):
		user = get_object_or_404(User, pk=self.userid)
		people = user.people
		return people
	
	class Meta:
		ordering = ['collect_time']
		verbose_name_plural = verbose_name = u'收藏'

class Agree(models.Model):
	userid = models.IntegerField(verbose_name=u'赞用户ID')
	messageid = models.IntegerField(verbose_name=u'微博ID')
	agree_time = models.DatetimeField(auto_now_add=True, verbose_name=u'赞时间')

	def __unicode__(self):
		return str(self.userid)+':'+str(self.messageid)
	
	def get_user(self):
		agree_user = get_object_or_404(User, pk=userid)
		people = agree_user.people
		return people
	
	class Meta:
		ordering = ['agree_time']
		verbose_name_plural = verbose_name = u'赞'


class Comment(models.Model):
	userid = models.IntegerField(verbose_name=u'评论用户')
	messageid = models.IntegerField(verbose_name=u'微博ID')
	content = models.CharField(max_length=280, verbose_name=u'评论内容')
	been_read = models.BooleanField(default=False, verbose_name=u'阅读状态')
	visible_status = models.IntegerField(default=0, verbose_name=u'可见状态')
	comment_time = models.DateTimeField(auto_now_add=True, verbose_name=u'评论时间')
	
	def __unicode__(self):
		return self.content
	
	def get_comment_author(self):
		user = get_object_or_404(User, pk=self.userid)
		author = user.people
		return author	

	def get_nickname(self):
		user = get_object_or_404(User, pk=self.userid)
		people = user.people
		return people.nickname

	def get_message(self)
		message = get_object_or_404(Message, pk=self.messageid)
		return message
	
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
		


