#-*- coding: utf-8 -*-
import os
import time
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponseRedirect
from message.models import Picture
from storage_images import local_uploaded_file
from upload_images import upload, remove

def upload_avatar(request):
	authuser = request.user
	people = authuser.people
	ext_allowed = ['jpg', 'jpeg', 'png']
	max_size = 1048576
	if 'avatar' not in request.FILES:
		return HttpResponseRedirect("/people/info")

	avatar = request.FILES['avatar']

	if not avatar or not avatar.name:
		return HttpResponseRedirect("/people/info")

	ext = avatar.name.split('.')[-1]
	if ext not in ext_allowed:
		return HttpResponseRedirect("/people/info")
	
	if avatar.size > max_size:
		return HttpResponseRedirect("/people/info")

	#STATIC_ROOT = os.path.join(os.path.dirname(__file__), '../static/')
	#user_avatar_dir = STATIC_ROOT+'%d/avatar/' % authuser.id 
	#if not os.path.exists(user_avatar_dir):
	#	os.makedirs(user_avatar_dir)

	#subfix = '%d/avatar/%s.%s' % (authuser.id, int(time.time()), ext)
	#path = STATIC_ROOT+subfix

	#path = local_uploaded_file(avatar, path)
	#path = '/static/'+subfix
	avatar_path = "user%d/avatar/%s.%s" % (authuser.id, int(time.time()), ext)
	old_avatar_url = people.avatar

	state = upload(avatar, avatar_path)
	if state == 'SUCCESS':
		QINIU_BASE_DOMAIN = 'http://7u2lxf.com1.z0.glb.clouddn.com/'
		path = QINIU_BASE_DOMAIN+avatar_path
		picture = Picture()
		picture.userid = authuser.id
		picture.picture_name = 'user%davatar%d' % ( authuser.id, int(time.time()))
		picture.picture_path = path 
		picture.save()
		people.avatar = path
		people.save()
		if Picture.objects.filter(picture_path=old_avatar_url):
			old_avatar_path = old_avatar_url.replace(QINIU_BASE_DOMAIN, '')
			remove(old_avatar_path)
			Picture.objects.filter(picture_path=old_avatar_url).delete()
	return HttpResponseRedirect("/people/info")

