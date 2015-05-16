#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import loader, RequestContext as TemplateRequestContext
from django.http import HttpResponse

from com.utils import AjaxData, paginate
from weilink.settings import MESSAGE_EACH_PAGE
from people.models import People, WlSettings, Relationship
from message.models import Message, Atuser, Comment, Agree
from letter.models import Letter
from letter.envelop import Envelop

@login_required(login_url="/login")
def get_reminder(request):
	user = request.user
	wlsettings = user.wlsettings 
	message_remind = wlsettings.message_remind
	if message_remind:
		beat_count = Atuser.objects.filter(useratid=user.id, benoticed=False).count()
		becomment_count = Comment.objects.filter(authorid=user.id, been_read=False).count()
		beagree_count = Agree.objects.filter(authorid=user.id, benoticed=False).count()
		letter_count = Letter.objects.filter(receiverid=user.id, been_read=False).count()
		new_fan_count = Relationship.objects.filter(wluserid=user.id, benoticed=False).count()
		total_count = beat_count+becomment_count+beagree_count+letter_count+new_fan_count
	else:
		beat_count = 0
		becomment_count = 0
		beagree_count = 0
		letter_count = 0
		new_fan_count = 0
		total_count = 0
	response_dict = {"message_remind": message_remind, "total": total_count, "atcount": beat_count, "commentcount": becomment_count, "agreecount": beagree_count, "lettercount": letter_count, "newfancount": new_fan_count}
	return AjaxData(response_dict)


@login_required(login_url="/login")
def message_at(request):
	user = request.user
	people = user.people
	Atuser.objects.filter(attype='M', benoticed=False).update(benoticed=True)
	atmsgid_query = Atuser.objects.filter(useratid=user.id, attype='M').values_list("objectid", flat=True)
	messages = Message.objects.filter(id__in=atmsgid_query)
	page = request.GET.get("page", "")
	message_list, paginator = paginate(messages, MESSAGE_EACH_PAGE, page)
	return render_to_response("people/atmsg.html", {"people": people, "message_list": message_list, "paginator": paginator}, RequestContext(request))


@login_required(login_url="/login")
def comment_at(request):
	user = request.user
	people = user.people
	atcomment_query = Atuser.objects.filter(useratid=user.id, attype='C').update(benoticed=True)
	atcomids = Atuser.objects.filter(useratid=user.id, attype='C').values_list("objectid", flat=True)
	comments = Comment.objects.filter(id__in=atcomids)
	page = request.GET.get("page", "")
	comment_list, paginator = paginate(comments, MESSAGE_EACH_PAGE, page)
	return render_to_response("people/atcomment.html", {"people": people, "comment_list": comment_list, "paginator": paginator})


@login_required(login_url="/login")
def received_comment(request):
	user = request.user
	people = user.people
	Comment.objects.filter(authorid=user.id, been_read=False).update(been_read=True)
	rcomment_query = Comment.objects.filter(authorid=user.id)
	page = request.GET.get("page", "")
	rcomment_list, paginator = paginate(rcomment_query, MESSAGE_EACH_PAGE, page)
	return render_to_response("people/comment_history.html", {"people": people, "comment_list": rcomment_list, "received": True, "paginator": paginator}, RequestContext(request))


@login_required(login_url="/login")
def sended_comment(request):
	user = request.user
	people = user.people
	scomment_query = Comment.objects.filter(userid=user.id)
	page = request.GET.get("page", "")
	scomment_list, paginator = paginate(scomment_query, MESSAGE_EACH_PAGE, page)
	return render_to_response("people/comment_history.html", {"people": people, "comment_list": scomment_list, "received": False, "paginator": paginator}, RequestContext(request))


@login_required(login_url="/login")
def agree_page(request):
	user = request.user
	people = user.people
	Agree.objects.filter(authorid=user.id, benoticed=False).update(benoticed=True)
	agree_query = Agree.objects.filter(authorid=user.id)
	page = request.GET.get("page", "")
	agree_list, paginator = paginate(agree_query, MESSAGE_EACH_PAGE, page)
	return render_to_response("people/agree_page.html", {"people": people, "agree_list": agree_list, "paginator": paginator}, RequestContext(request))


@login_required(login_url="/login")
def letter_page(request):
	authuser=request.user
	people = authuser.people
	raw_senderid_list = Letter.objects.filter(receiverid=authuser.id, been_read=False).values_list('senderid', flat=True)
	senderid_list = list(set(raw_senderid_list))
	envelop_list = []
	for sid in senderid_list:
		sender = get_object_or_404(People, user_id=sid)
		letter = Letter.objects.filter(receiverid=authuser.id, senderid=sid, been_read=False)[0]
		count = Letter.objects.filter(receiverid=authuser.id, senderid=sid, been_read=False).count()
		envelop = Envelop(sender, letter, count)
		envelop_list.append(envelop)
	return render_to_response("people/letter_page.html", {"people": people, "envelop_list": envelop_list}, RequestContext(request))


@login_required(login_url="/login")
def recent_contact(request):
	authuser = request.user
	raw_sid_list = Letter.objects.filter(receiverid=authuser.id).values_list('senderid', flat=True)
	raw_rid_list = Letter.objects.filter(senderid=authuser.id).values_list('receiverid', flat=True)
	sid_list = list(set(raw_sid_list))
	rid_list = list(set(raw_rid_list))
	sid_list.extend(rid_list)
	friendid_list = list(set(sid_list))
	friend_list = People.objects.filter(user_id__in=friendid_list)
	template = loader.get_template("people/recent_contact.html")
	context = TemplateRequestContext(request, {"friend_list": friend_list})
	return HttpResponse(template.render(context))


	
	








