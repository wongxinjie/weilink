#-*- coding: utf-8 -*-
import re

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class Retweet(models.Model):
	originalid = models.IntegerField(verbose_name=u'源id')
	retweetmsgid = models.IntegerField(verbose_name=u'转发ID')
	
	def __unicode__(self):
		return str(originalid)+':'+str(retweetmsgid)

	class Meta:
		verbose_name_plural = verbose_name=u'转发'


class Message(models.Model):
	author = models.ForeignKey(User, verbose_name=u'用户')
	message_type = models.IntegerField(default=0, verbose_name=u'微博类型')
	isoriginal = models.BooleanField(default=True, verbose_name=u'原创')
	private = models.BooleanField(default=False, verbose_name=u'自己可见')
	content = models.CharField(max_length=280, verbose_name=u'微博内容')
	publish_time = models.DateTimeField(auto_now_add=True, verbose_name=u'发布时间')
	collect_count = models.IntegerField(default=0, verbose_name=u'收藏次数')
	comment_count = models.IntegerField(default=0, verbose_name=u'评论次数')
	retweet_count = models.IntegerField(default=0, verbose_name=u'转发次数')
	agree_count = models.IntegerField(default=0, verbose_name=u'赞次数')
	read_count = models.IntegerField(default=0, verbose_name=u'阅读次数')
	
	def __unicode__(self):
		return self.content

	def get_author(self):
		people = self.author.people
		return people
	
	def get_nickname(self):
		people = self.author.people
		return people.nickname

	def get_avatar(self):
		people = self.author.people
		return people.avatar
	
	def get_retweet_text(self):
		people = self.author.people
		nickname = people.nickname
		aprefix = re.compile(r'<a href="/people/profile/(\d+)" class="atlink">', re.I)
		asubfix = re.compile(r'</a>', re.I)
		content = aprefix.sub('', self.content)
		content = asubfix.sub('', content)
		retweet_text = '//@'+nickname+':'+content
		return retweet_text

	def get_original_msg(self):
		originalids = Retweet.objects.filter(retweetmsgid=self.id).values_list('originalid', flat=True)
		originalmsg = []	
		for originalid in originalids:
			msg = get_object_or_404(Message, pk=originalid)
			if msg.isoriginal:
				originalmsg.append(msg)
		if originalmsg:
			return originalmsg[0]
		else:
			return None
			
			
				
	class Meta:
		ordering = ['-publish_time']
		verbose_name_plural = verbose_name = u'微博'

class Atuser(models.Model):
	ATTYPE_CHOICES = (
		(u'M', u'message'), 
		(u'C', u'comment'), 
	)

	attype = models.CharField(max_length=4, choices=ATTYPE_CHOICES, verbose_name=u'类型')
	objectid = models.IntegerField(blank=True, verbose_name=u'消息评论ID')
	atuserid = models.IntegerField(verbose_name=u'AT用户')
	useratid = models.IntegerField(verbose_name=u'被AT用户')
	benoticed = models.BooleanField(default=False, verbose_name=u'已提醒')
	attime = models.DateTimeField(auto_now_add=True, verbose_name=u'AT时间')

	
	def __unicode__(self):
		return str(self.atuserid)+'@'+str(self.useratid)
	
	def get_message(self):
		message = get_object_or_404(Message,  pk=self.messageid)
		return message

	def get_original_msg(self):
		message = self.get_message()
		orimsg = message.get_original_msg()
		return orimsg
	
	def get_atuser(self):
		user = get_object_or_404(User, pk=self.atuserid)
		people = user.people
		return people
	
	class Meta:
		ordering = ['-attime']
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
		ordering = ['-collect_time']
		verbose_name_plural = verbose_name = u'收藏'

class Agree(models.Model):
	userid = models.IntegerField(verbose_name=u'赞用户ID')
	authorid = models.IntegerField(verbose_name=u'作者ID')
	messageid = models.IntegerField(verbose_name=u'微博ID')
	benoticed = models.BooleanField(default=False, verbose_name=u'已提醒')
	agree_time = models.DateTimeField(auto_now_add=True, verbose_name=u'赞时间')

	def __unicode__(self):
		return str(self.userid)+':'+str(self.messageid)
	
	def get_user(self):
		agree_user = get_object_or_404(User, pk=self.userid)
		people = agree_user.people
		return people

	def get_author(self):
		agree_author = get_object_or_404(User, pk=self.authorid)
		people = agree_author.people
		return people

	def get_message(self):
		message = get_object_or_404(Message, pk=self.messageid)
		return message
	
	class Meta:
		ordering = ['-agree_time']
		verbose_name_plural = verbose_name = u'赞'


class Comment(models.Model):
	userid = models.IntegerField(verbose_name=u'评论用户')
	authorid = models.IntegerField(verbose_name=u'作者ID')
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

	def get_message(self):
		message = get_object_or_404(Message, pk=self.messageid)
		return message

	def get_message_author(self):
		msguser = get_object_or_404(User, pk=self.authorid)
		message_author = msguser.people
		return message_author
	
	class Meta:
		ordering = ['-comment_time']
		verbose_name_plural = verbose_name=u'评论'
	

class Picture(models.Model):
	userid = models.IntegerField(verbose_name=u'用户ID')
	picture_name = models.CharField(max_length=100, verbose_name=u'图片名')
	picture_path = models.CharField(max_length=200, default='', verbose_name=u'图片路径')
	visible_status = models.IntegerField(default=0, verbose_name=u'可见状态')
	add_time = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')

	def __unicode__(self):
		return self.picture_name
	
	class Meta:
		ordering = ['add_time']
		verbose_name_plural = verbose_name=u'图片'
		
class MessagePicture(models.Model):
	pictureid = models.IntegerField(verbose_name=u'图片ID')
	messageid = models.IntegerField(verbose_name=u'消息ID')

	def __unicode__(self):
		return str(self.pictureid)+"p:m"+str(self.messageid)

	class Meta: 
		ordering = ['id']
		verbose_name_plural = verbose_name = u'推文配图'





