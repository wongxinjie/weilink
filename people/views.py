#-*- coding: utf-8 -*-
from datetime import date

from django.shortcuts import render_to_response, get_object_or_404, RequestContext, redirect, render
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db.models import Q
from django.contrib.auth import logout 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import People, Relationship, Blacklist
from message.models import Message


def profile(request, pid):
	people = get_object_or_404(People, pk=pid)
	user = people.user
	if request.user.is_authenticated() and request.user.id == user.id:
		message_list = user.message_set.all()
	else:
		message_list = user.message_set.filter(private=False)

	paginator = Paginator(message_list, 20)	
	page = request.GET.get("page", "")
	try:
		messages = paginator.page(page)
	except PageNotAnInteger:
		messages = paginator.page(1)
	except EmptyPage:
		messages = paginator.page(paginator.num_pages)
	
	message_num = user.message_set.all().count()
	follow_num = Relationship.objects.filter(followerid=user.id).count()
	follower_num = Relationship.objects.filter(wluserid=user.id).count()
	
	return render_to_response("user/profile.html", {"messages": messages, "message_num": message_num, "follow_num": follow_num, "follower_num": follower_num}, RequestContext(request))


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
	return HttpResponseRedirect("/people/%d/home" % people.id)
	

@login_required(login_url="/login")
def home(request, pid):
	people = get_object_or_404(People, pk=pid)
	
	
	
	
		

	
	



	
	
	
		
	
		
	
	
	


