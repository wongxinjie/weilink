#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, RequestContext, redirect, render
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResposneRedirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from com.utils import paginate, AjaxData,  AjaxWarn, AjaxFail, AjaxSuccess, AjaxJump
from people.models import People, Blacklist
from models import Message, Comment, Collection, Agree
import services 

def show_message(request, mid):
	message = get_object_or_404(Message, pk=mid)
	comments = Comment.objects.filter(messageid=message.id)
	return render_to_response("user/message.html", {"message": message, "comments": comments}, RequestContext(request))


def get_comment_list(request):
	mid = request.POST.get("mid", "")

	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer")
	
	mid = int(mid)
	comment_queryset = Comment.objects.filter(messageid=mid)
	comment_list = []
	for comment in comment_queryset:
		cdict = {}
		cdict['pid'] = comment.get_user().id
		cdict['nickname'] = smart_str(comment.get_nickname())
		cdict['content'] = smart_str(comment.content)
		cdict['comment_time'] = comment.comment_time
		comment_list.append(cdict)

	response_data = {}
	response_data['comment_list'] = comment_list	
	return AjaxData(response_data)


def get_retweet_list(request):
	mid = request.POST.get("mid", "")
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer")
	
	mid = int(mid)
	retweet_queryset = Message.objects.filter(isoriginal=False, originalid=mid)
	retweet_list = []
	for retweet in retweet_queryset:
		rdict = {}
		rdict['pid'] = retweet.get_author().id
		rdict['nickname'] = smart_str(retweet.get_nickname())
		rdict['content'] = smart_str(retweet.content)
		rdict['retweet_time'] = retweet.pulish_time
		retweet_list.append(rdict)
	
	response_data = {}
	response_data['retweet_list'] = retweet_list
	return AjaxData(response_data)

def get_agree_list(request):
	mid = request.POST.get("mid", "")
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer")
	
	mid = int(mid)
	agree_queryset = Agree.objects.filter(messageid=mid)
	agree_list = []
	for agree in agree_queryset:
		adict = {}
		adict['pid'] = agree.get_user().id
		adict['nickname'] = agree.get_user().nickname
		agree_list.append(adict)
	
	response_data = {}
	resposne_data['agree_list'] = agree_list
	return AjaxData(response_data)
	

@login_required(login_url="/login")
def post_message(request):
	visible_status = request.POST.get("visible", "")
	content = request.POST.get("content", "").strip()
		
	if not content:
		return AjaxWarn("content empty!")
	
	message = Message()
	if visible_status == 'private':
		message.private = True
	message.author = request.user
	message.content = content
	message.save()
	services.process_content(request.user, content, 'M', message.id)	
	return AjaxSuccess("post message success !")


@login_required(login_url="/login")
def remove_message(request):
	mid = request.POST.get("mid", "")
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid empty!")
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	#
	Atuser.objects.filter(messageid=mid).delete()
	Collection.objects.filter(messageid=mid).delete()
	#
	if message.isoriginal:
		Message.objects.filter(isoriginal=False, originalid=message.id).update(originalid=0)
	else:
		Message.objects.filter(isoriginal=False, originalid=message.id).update(originalid=message.originalid)
			
	Message.objects.filter(id=mid).delete()
	return AjaxSuccess("Success !")


@login_required(login_url="/login")
def post_comment(request):
	mid = request.POST.get("mid", "")
	content = request.POST.get("content", "").strip()
	
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer!")
	
	mid = int(mid)
	if not content:
		return AjaxWarn("content empty!") 

	comment = Comment()
	comment.userid = request.user.id
	comment.messageid = mid
	comment.content = content 
	comment.save()
	services.process_content(request.user, content, 'C', comment.id)
	
	message = get_object_or_404(Message, pk=mid)
	message.comment_count += 1
	message.save()	
	return AjaxSuccess("post comment success!")


@login_required(login_url="/login")
def reomve_comment(request):
	cmid = request.POST.get("cmid", "")
	if not(cmid and cmid.isdigit()):
		return AjaxWarn("cmid not an integer!")
	cmid = int(cmid)

	msssage = get_object_or_404(Message, pk=mid)
	message.comment_count -= 1
	message.save()	
	
	Atuser.objects.filter(commentid=cmid).delete()
	Comment.objects.filter(id=cmid).delete()
	return AjaxSuccess("success!")


@login_required(login_url="/login")
def retweet(request):
	mid = request.POST.get("mid", "")
	content = request.POST.get("content", "").strip()
	visible_status = request.POST.get("visible", "")
	
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer!")
	
	if not content:
		return AjaxWarn("content empty!")

	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	rmsg = Message()
	rmsg.author = request.user
	rmsg.isoriginal = False
	rmsg.originalid = mid
	rmsg.content = content
	rmsg.save()
	
	message.retweet_count += 1
	message.save()
	while not message.isoriginal:
		message = get_object_or_404(Message, pk=originalid)
		message.retweet_count += 1
		message.save()
	message.retweet_count += 1

	process_retweet_content(request.user, content, rmsg.id)
	return AjaxSuccess("success !")


@login_required(login_url="/login")
def add_collection(request):
	mid = request.POST.get("mid", "")

	if not(mid and mid.isdigit()):
		return AjaxWarn("mid empty!")
	
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)

	collection = Collection()
	collection.userid = request.user.id
	collection.messageid = mid
	collection.save()
	
	message.collect_count += 1
	message.save()
	
	return AjaxSuccess("success !")


@login_required(login_url="/login")
def remove_collection(request):
	clid = request.POST.get("clid", "")
	
	if not(clid and clid.isdigit()):
		return AjaxWarn("clid empty!")
	
	clid = int(clid)
	collection = get_object_or_404(Collection, pk=clid)
	message = get_object_or_404(Message, pk=collection.messageid)
	message.collect_count -= 1
	message.save()
	
	collection.delete()
	return AjaxSuccess("remove success!")
	

@login_required(login_url="/login")
def agree(request):
	mid = request.POST.get("mid", "")
	
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid empty!")
	
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	authuser = request.user
	agree_queryset = Agree.objects.filter(userid=authuser.id, messageid=mid)
	if agree_queryset:
		message.agree_count -= 1
		message.save()
		agree_queryset.delete()
	else:
		message.agree_count += 1
		message.save()
		agree = Agree()
		agree.userid = authuser.id
		agree.messageid = mid
		agree.save()
	return AjaxSuccess("success!")


@login_required(login_url="/login")
def collections(request):
	authuser = request.user
	collections = Collection.objects.filter(userid=authuser.id)
	
	page = request.GET.get("page", "")
	collection_list = paginate(collections, MESSAGE_EACH_PAGE, page)
	return render_to_response("user/collection.html", {"collection_list": collection_list})


@login_required(login_url="/login")
def atmessage(request):
	authuser = request.user
	atmsgs = Atuser.objects.filter(attype='M', useratid=authuser.id)
	page = request.GET.get("page", "")
	atmsg_list = paginate(atmsgs, MESSAGE_EACH_PAGE, page)
	return render_to_response("user/atinfo.html", {"atmsg_list": atmsg_list})
	

@login_required(login_url="/login")
def atcomment(request):
	atthuser = request.user
	atcomments = Atuser.objects.filter(attype='C', useratid=authuser.id)
	page = request.GET.get("page", "")
	atcomment_list = paginate(atcomments, MESSAGE_EACH_PAGE, page)
	return render_to_response("user/atinfo.html", {"atcomment_list": atcomment_list})

	
	
