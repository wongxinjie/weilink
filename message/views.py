#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, RequestContext, redirect, render
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, RequestContext as TemplateRequestContext

from weilink.settings import COMMENT_EACH_PAGE, RETWEET_EACH_PAGE, MESSAGE_EACH_PAGE
from com.utils import paginate, AjaxData,  AjaxWarn, AjaxFail, AjaxSuccess, AjaxJump, AjaxAlert
from com.clean_context import clean_data, get_original_data
from com.repute import update_reputation
from com.iptool import get_location
from people.models import People, Blacklist, Relationship, Whitelist, WlSettings 
from models import Message, Comment, Collection, Agree, Atuser, Retweet
import services 

def show_message(request, mid):
	if request.user.is_authenticated():
		authuser = request.user
		people = authuser.people
		message = get_object_or_404(Message, pk=mid)
		comments = Comment.objects.filter(messageid=mid)
		author = get_object_or_404(User, pk=message.author.id)
		request_people = author.people
		putlist = Blacklist.objects.filter(wluserid=authuser.id, blackerid=author.id).count() > 0
		onlist = Blacklist.objects.filter(wluserid=author.id, blackerid=authuser.id).count() > 0
		if putlist or onlist:
			state = "BLACKLIST"
		else: 
			state = ""
		wlsettings = author.wlsettings
		if wlsettings.account_mode == 'N':
			show = "HIDDEN"
		elif wlsettings.account_mode == 'S':
			befollowed = Relationship.objects.filter(wluserid = authuser.id, followerid=author.id)
			onwhitelist = str(authuser.id)+',' in author.whitelist.white_list
			if not (befollowed or onwhitelist):
				show = "HIDDEN"
			else:
				show = ""
		else:
			show = ""
	else:
		message = get_object_or_404(Message, pk=mid)
		comments = Comment.objects.filter(messageid=mid)
		author = get_object_or_404(User, pk=message.author.id)
		request_people = author.people
		people=None
		state = ""
		show = ""
	return render_to_response("people/message.html", {"message": message, "comments": comments, "request_people": request_people, "people": people, "state": state, "show": show}, RequestContext(request))


@login_required(login_url="/login")
@csrf_exempt
def get_comment_list(request):
	mid = request.POST.get("mid", "")
	home = request.POST.get("home", "")

	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer")
	
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	comments = Comment.objects.filter(messageid=mid)
	people = request.user.people
	template = loader.get_template("people/comments.html")
	if home:
		context = TemplateRequestContext(request, {"message": message, "comments": comments, "people": people})
	else:
		context = TemplateRequestContext(request, {"comments": comments, "people":people})
	return HttpResponse(template.render(context))


@login_required(login_url="/login")
@csrf_exempt
def get_retweet_list(request):
	mid = request.POST.get("mid", "")
	home = request.POST.get("home", "")
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer")
	
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	retweetid_queryset = Retweet.objects.filter(originalid = mid).values_list('retweetmsgid', flat=True)
	retweetmsgs = Message.objects.filter(id__in = retweetid_queryset)
	template = loader.get_template("people/retweets.html")
	if home:
		retweet_count = len(retweetmsgs)
		context = TemplateRequestContext(request, {"message": message, "retweet_count": retweet_count})
	else:
		context = TemplateRequestContext(request, {"retweets": retweetmsgs})
	return HttpResponse(template.render(context))


@login_required(login_url="/login")
@csrf_exempt
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
	if request.META.has_key('HTTP_X_FORWARDED_FOR'):
		ip = request.META['HTTP_X_FORWARDED_FOR']
	else:
		ip = request.META['REMOTE_ADDR']
	realip = ip.split(',')[0]
	location = get_location(realip)
	if not location:
		message.location = ''
		location = ''
	else:
		message.location = location.split(',')[-1]
	message.author = request.user
	message.content = content
	message.save()
	authuser = request.user
	people = authuser.people
	repu = people.reputation
	update_reputation(repu, "TWEET", location)
	if visible_status == 'N':
		message.private = True
		message.save()
	content = clean_data(content)
	if not message.private:
		content = services.process_content(request.user, content, 'M', message.id)	
	content = services.process_content_link(content)
	message.content = content
	message.save()
	template = loader.get_template("people/message_cut.html")
	context = TemplateRequestContext(request, {"message": message})
	return HttpResponse(template.render(context))


@login_required(login_url="/login")
@csrf_exempt
def remove_message(request):
	authuser = request.user
	people = authuser.people
	mid = request.POST.get("mid", "")
	if not(mid and mid.isdigit()):
		return AjaxWarn("参数错误!")
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	if message.author.id != request.user.id:
		return AjaxAlert("权限错误!")

	Atuser.objects.filter(attype='M', objectid=mid).delete()
	Collection.objects.filter(messageid=mid).delete()
	Comment.objects.filter(messageid=mid).delete()
	Agree.objects.filter(messageid=mid).delete()
	Retweet.objects.filter(originalid=mid).delete()
	
	originalids = Retweet.objects.filter(retweetmsgid=mid).values_list('originalid', flat=True)
	originalmsg_queryset = Message.objects.filter(id__in=originalids)		
	
	for originalmsg in originalmsg_queryset:
		originalmsg.retweet_count = F('retweet_count') - 1
		originalmsg.save()
	
	Retweet.objects.filter(retweetmsgid=mid).delete()
	Message.objects.filter(id=mid).delete()
	update_reputation(people.reputation, "DELETE")
	return AjaxSuccess("Success!")


@login_required(login_url="/login")
def post_comment(request):
	mid = request.POST.get("mid", "")
	content = request.POST.get("content", "").strip()
	reply_sub = request.POST.get("reply_sub", "").strip()
	
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer!")
	
	mid = int(mid)
	if not content:
		return AjaxWarn("评论内容不能为空!") 
	if reply_sub:
		content = reply_sub+content

	message = get_object_or_404(Message, pk=mid)
	message.comment_count = F('comment_count') + 1
	message.save()	

	template = loader.get_template("people/comment_cut.html")
	comment = Comment()
	comment.userid = request.user.id
	comment.authorid = message.author.id
	comment.messageid = mid
	comment.content = content 
	comment.save()
	if comment.userid == comment.authorid:
		comment.been_read=True
		comment.save()
	content = clean_data(content)
	content = services.process_content(request.user, content, 'C', comment.id)
	comment.content = content
	comment.save()
	context = TemplateRequestContext(request, {"comment": comment })
	if reply_sub:
		return AjaxSuccess("回复成功！")
	return HttpResponse(template.render(context))
	 

@login_required(login_url="/login")
@csrf_exempt
def remove_comment(request):
	cmid = request.POST.get("cmid", "")
	if not(cmid and cmid.isdigit()):
		return AjaxWarn("cmid not an integer!")
	cmid = int(cmid)
	
	comment = get_object_or_404(Comment, pk=cmid)
	message = get_object_or_404(Message, pk=comment.messageid)

	authuser = request.user
	if not(authuser.id == comment.userid or authuser.id == message.author.id):
		return AjaxWarn("您没有权限!")

	message.comment_count = F('comment_count') - 1
	message.save()	
	
	Atuser.objects.filter(attype='C', objectid=cmid).delete()
	Comment.objects.filter(id=cmid).delete()
	return AjaxSuccess("success!")


@login_required(login_url="/login")
def retweet(request):
	mid = request.POST.get("mid", "")
	content = request.POST.get("content", "").strip()
	home = request.POST.get("home", "").strip()
	
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid not an integer!")
	
	if not content:
		return AjaxWarn("content empty!")

	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	rmsg = Message()
	rmsg.author = request.user
	rmsg.isoriginal = False
	rmsg.content = content
	rmsg.save()

	message.retweet_count = F('retweet_count') + 1
	message.save()

	retweet = Retweet(originalid=message.id, retweetmsgid=rmsg.id)
	retweet.save()

	content = clean_data(content)
	content = services.process_retweet_content(request.user, content, rmsg.id)
	rmsg.content = content
	rmsg.save()
	
	if not message.isoriginal:
		originalmsgid_list = Retweet.objects.filter(retweetmsgid=message.id).values_list('originalid', flat=True)
		for originalmsgid in originalmsgid_list:
			retweet = Retweet(originalid=originalmsgid, retweetmsgid=rmsg.id)
			retweet.save()
			originalmsg = get_object_or_404(Message, pk=originalmsgid)
			originalmsg.retweet_count = F('retweet_count') + 1
			originalmsg.save()

	if request.META.has_key('HTTP_X_FORWARDED_FOR'):
		ip = request.META['HTTP_X_FORWARDED_FOR']
	else:
		ip = request.META['REMOTE_ADDR']
	realip = ip.split(',')[0]
	location = get_location(realip)
	if not location:
		rmsg.location = ''
		location = ''
	else:
		rmsg.location = location.split(',')[-1]
	rmsg.save()

	if home:
		template = loader.get_template("people/message_cut.html")
		context = TemplateRequestContext(request, {"message": rmsg})
	else:
		template = loader.get_template("people/retweet_cut.html")
		context = TemplateRequestContext(request, {"retweet": rmsg})
	return HttpResponse(template.render(context))


@login_required(login_url="/login")
@csrf_exempt
def collect(request):
	mid = request.POST.get("mid", "")

	if not(mid and mid.isdigit()):
		return AjaxWarn("参数错误!")
	
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	
	collection_queryset = Collection.objects.filter(userid=request.user.id, messageid=mid)
	if collection_queryset:
		Collection.objects.filter(userid=request.user.id, messageid=mid).delete()
		message.collect_count = F('collect_count') - 1
		message.save()
		resmsg = u'收藏'
	else:
		collection = Collection()
		collection.userid = request.user.id
		collection.messageid = mid
		collection.save()
		message.collect_count = F('collect_count') + 1
		message.save()
		resmsg = u'已收藏'
	return AjaxSuccess(resmsg)


@login_required(login_url="/login")
@csrf_exempt
def agree(request):
	mid = request.POST.get("mid", "")
	
	if not(mid and mid.isdigit()):
		return AjaxWarn("mid empty!")
	
	mid = int(mid)
	message = get_object_or_404(Message, pk=mid)
	authuser = request.user
	agree_queryset = Agree.objects.filter(userid=authuser.id, messageid=mid)
	if agree_queryset:
		message.agree_count = F('agree_count') - 1
		message.save()
		agree_queryset.delete()
	else:
		message.agree_count = F('agree_count') + 1
		message.save()
		agree = Agree()
		agree.userid = authuser.id
		agree.authorid = message.author.id
		agree.messageid = mid
		agree.save()
	return AjaxSuccess("success!")


@login_required(login_url="/login")
def collections(request):
	authuser = request.user
	people = authuser.people
	collections = Collection.objects.filter(userid=authuser.id)
	
	page = request.GET.get("page", "")
	collection_list, paginator = paginate(collections, MESSAGE_EACH_PAGE, page)
	message_list = [ collection.get_message for collection in collection_list ]
	return render_to_response("people/collection.html", {"collection_list": collection_list, "message_list": message_list, "paginator": paginator, "people": people})


@login_required(login_url="/login")
def agrees(request):
	authuser = request.user
	people = authuser.people
	agreements = Agree.objects.filter(userid=authuser.id)
	
	page = request.GET.get("page", "")
	agreements, paginator = paginate(agreements, MESSAGE_EACH_PAGE, page)
	message_list = [ agreement.get_message for agreement in agreements]
	return render_to_response("people/agree.html", {"agree_list": agreements, "message_list": message_list, "paginator": paginator, "people": people})


@login_required(login_url="/login")
@csrf_exempt
def get_reply_form(request):
	authuser = request.user
	cmid = request.POST.get("cmid", "")
	if not(cmid and cmid.isdigit()):
		return AjaxWarn("Params error!")

	cmid = int(cmid)
	comment = get_object_or_404(Comment, pk=cmid)
	message = comment.get_message()
	author = comment.get_comment_author()
	template = loader.get_template("people/reply_comment_cut.html")
	context = TemplateRequestContext(request, {"comment": comment, "message": message, "author": author})
	return HttpResponse(template.render(context))










	
	
