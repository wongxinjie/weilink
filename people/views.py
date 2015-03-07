#-*- coding: utf-8 -*-
from datetime import date

from django.shortcuts import render_to_response, get_object_or_404, RequestContext, redirect, render
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth import logout 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from weilink.settings import MESSAGE_EACH_PAGE, FOLLOW_EACH_PAGE, FAN_EACH_PAGE
from message.models import Message
from com.utils import paginate, AjaxData, AjaxWarn, AjaxFail, AjaxSuccess, AjaxJump
from models import People, Relationship, Blacklist
import services


def profile(request, pid):
	people = get_object_or_404(People, pk=pid)
	user = people.user
	if request.user.is_authenticated() and request.user.id == user.id:
		message_list = user.message_set.all()
	else:
		message_list = user.message_set.filter(private=False)

	page = request.GET.get("page", "")
	messages = services.paginate(message_list, MESSAGE_EACH_PAGE, page)
	
	message_num = user.message_set.all().count()
	follow_num = Relationship.objects.filter(followerid=user.id).count()
	follower_num = Relationship.objects.filter(wluserid=user.id).count()
	
	return render_to_response("user/profile.html", {"messages": messages, "message_num": message_num, "follow_num": follow_num, "follower_num": follower_num}, RequestContext(request))


@login_required(login_url="/login")
def logout(request):
	logout(request)
	return HttpResponseRedirect("/login")


@login_required(login_url="/loign")
def fillinfo(request):
	if request.method == 'GET':
		people = request.user.people
		return render_to_response("user/fillinfo.html", {"people": people}, RequestContext(request))
	nickname = request.POST.get("nickname", "").strip()
	realname = request.POST.get("realname", "").strip()
	address = request.POST.get("address", "").strip()
	gender = request.POST.get("gender", "")
	sexual = request.POST.get("sexual", "")
	feeling = request.POST.get("feeling", "")
	birthday = request.POST.get("birthday", "")
	domainurl = request.POST.get("domainurl", "").strip()
	introduction = request.POST.get("introduction", "").strip()
	contact_email = request.POST.get("email", "").strip()
	QQ = request.POST.get("qq", "").strip()
	wechat = request.POST.get("wechat", "").strip()
	profession = request.POST.get("profession", "").strip()
	label = request.POST.get("label", "").strip()
	
	if nickname:
		people.nickname = nickname
	if realname:
		people.realname = realname
	if address:
		people.address = address
	if gender and gender in 'UFM':
		people.gender = gender
	if sexual and sexual in 'SHBU':
		people.sexual = sexual
	if feeling and feeling in 'SAIEDU':
		people.feeling = feeling
	if birthday:
		date_list = birthday.split('-')
		birthdate = date(date_list[0], date_list[1], date_list[2])
		people.birthday = birthdate
	if domainurl:
		people.domainurl = domainurl
	if introduction:
		people.introduction = introduction
	if contact_email:
		people.contact_email = contact_email
	if QQ:
		people.QQ = QQ
	if wechat:
		people.wechat = wechat
	if profession:
		people.profession = profession
	if label:
		people.label = label 
	people.save()
	return HttpResponseRedirect("/people/home")
	

@login_required(login_url="/login")
def home(request):
	user = request.user
	people = user.people 
	recent_messageids = services.get_recent_messageids(user)
	
	page = request.GET.get("page", "")
	single_messageids = services.paginate(recent_messageids, MESSAGE_EACH_PAGE, page)
	message_id_list = single_messageids.object_list
	message_list = Message.objects.filter(id__in=message_id_list)
	message_num = user.message_set.all().count()
	follow_num = Relationship.objects.filter(followerid=user.id).count()
	follower_num = Relationship.objects.filter(wluserid=user.id).count()
	return render_to_response("user/home.html", {"people": people, "message_list": message_list, "message_num": message_num, "follow_num": follow_num, "follower_num": follower_num}, RequestContext(request))


@login_required(login_url="/login")
def set_info(request):
	return render_to_response("user/set.html", RequestContext(request))

@login_required(login_url="/login")
def follow_page(request):
	authuser = request.user
	follow_queryset = Relationship.objects.filter(followerid=authuser)
	follow_num = follow_queryset.count()
	follow_id_list = [ r.wluserid for r in follow_queryset]
	follows = People.objects.filter(user_id__in=follow_id_list)
	
	page = request.GET.get("page", "")
	follow_list = paginate(follows, FOLLOW_EACH_PAGE, page)
	return render_to_response("user/follow.html", {"follow_list": follow_list, "follow_num": follow_num})


@login_required(login_url="/login")
def fan_page(request):
	authuser = request.user
	fan_queryset = Relationship.objects.filter(wluserid=authuser.id)
	fan_num = fan_queryset.count()
	fan_id_list = [ r.followerid for r in fan_queryset]
	fans = People.objects.filter(user_id__in=fan_id_list)
	
	page = request.GET.get("page", "")
	fan_list = paginate(fans, FAN_EACH_PAGE, page)
	return render_to_response("user/fan.html", {"fan_list": fan_list, "fan_num": fan_num})


@login_required(login_url="/login")
def add_follow(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("pid empty!")

	pid = int(pid)
	fpeople = get_object_or_404(People, pk=pid)
	fuser = fpeople.user
	authuser = request.user

	if Blacklist.objects.filter(wluserid=fuser.id, blackerid=authuser.id):
		return AjaxAlert("You are on the list! Fail!")

	relationship = Relationship(wluserid=fuser.id, followerid=authuser.id)
	relationship.save()
	return AjaxSuccess("add follow success!")


@login_required(login_url="/login")
def remove_follow(request):
	pid = request.POST.get("pid", "")
	if not (pid and pid.isdigit()):
		return AjaxWarn("pid empty!")
	pid = int(pid)
	fpeople = get_object_or_404(People, pk=pid)
	fuser = fpeople.user
	Relationship.objects.filter(wluserid=fuser.id, followerid=request.user.id).delete()
	return AjaxSuccess("remote follow success!")


@login_required(login_url="/login")
def remove_fan(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("pid empty!")
	pid = int(pid)
	bfpeople = get_object_or_404(People, pk=pid)
	bfuser = bfpeople.user
	Relationship.objects.filter(wluserid=request.user.id, followerid=bfuser.id).delete()
	return AjaxSuccess("remote follower success!")


@login_required(login_url="/login")
def add_blacklist(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("pid empty!")
	
	pid = int(pid)
	fpeople = get_object_or_404(People, pk=pid)
	fuser = fpeople.user
	authuser = request.user
	
	Relationship.objects.filter(wluserid=fuser.id, followerid=authuser.id).delete()
	Relationship.objects.filter(wluserid=authuser.id, followerid=fuser.id).delete()

	blacklist = Blacklist(wluserid=authuser.id, blackerid=fuser.id)
	blacklist.save()
	
	return AjaxSuccess("add blacklist success!")

@login_required(login_url="/login")
def remove_blacklist(request):
	pid = request.POST.get("pid", "")
	if not(pid and pid.isdigit()):
		return AjaxWarn("pid empty!")
	
	pid = int(pid)
	bpeople = get_object_or_404(People, pk=pid)
	buser = bpeople.user
	
	Blacklist.objects.filter(wluserid=request.user.id, blackerid=buser.id).delete()
	return AjaxSuccess("remove blacklist success!")


