#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, RequestContext, redirect, render
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from weilink.settings import LETTER_EACH_PAGE
from com.utils import paginate, AjaxData, AjaxWarn, AjaxFail, AjaxSuccess, AjaxJump
from people.models import People, Blacklist
from models import Letter


@login_required(login_url="/login")
def send_letter(request):
	authuser = request.user
	rid = request.POST.get("rid", "")
	content = request.POST.get("content", "").strip()
	
	if not(rid and rid.isdigit()):
		return AjaxWarn("rid not an integer!")
	
	if not content:
		return AjaxWarn("content empty!")
	
	rid = int(rid)
	receiver = get_object_or_404(User, pk=rid)
	onblacklist = Blacklist.objects.filter(wluserid=receiver.id, blackerid=authuser.id)
	if onblacklist:
		return AjaxAlert("on the list!")
	
	letter = Letter()
	letter.senderid = authuser.id
	letter.receiverid = receiver.id
	letter.content = content
	letter.save()
	return AjaxSuccess("success!")


@login_required(login_url="/login")
def history_letters(request, pid):
	sender = request.user
	people = get_object_or_404(People, pk=rid)
	receiver = people.user

	sletter_qset = Letter.objects.filter(senderid=sender.id, receiverid=receiver.id, sender_delete=False)	
	rletter_qset = Letter.objects.filter(senderid=receiver.id, receiverid=sender.id, receiver_delete=False)

	history_letters = list(sletter_qset)
	history_letters.extend(list(rletter_qset))
	history_letters.sort(key = lambda x: x.send_time)

	page = request.POST.get("page", "")
	if not(page and page.isdigit()):
		page = len(history_letters)/LETTER_EACH_PAGE + 1
	
	letters = paginate(history_letters, LETTER_EACH_PAGE, page)
	letter_list = []
	for letter in letters:
		ldict = {}
		ldict['nickname'] = smart_str(letter.get_sender().nickname)
		ldict['content'] = smart_str(letter.content)
		ldict['send_time'] = letter.send_time
		letter_list.append(ldict)
	response_dict['letter_list'] = letter_list
	return AjaxData(response_dict)


@login_required(login_url="/login")
def letter_page(request):
	authuser = request.user
	new_letters = Letter.objects.filter(been_read=False)
	letters = Letter.objects.filter(senderid=authuser.id)
	people_list = [ letter.get_receiver() for letter in letters]
	return render_to_response("user/letters.html", {"people_list": people_list, "new_letters": new_letters}, RequestContext(request))


@login_required(login_url="/login")
def remove_letters(request, pid):
	sender = request.user
	people = get_object_or_404(People, pk=pid)
	receiver = people.user
	Letter.objects.filter(senderid=sender.id, receiverid=receiver.id).update(sender_delete=True)
	Letter.objects.filter(senderid=receiver.id, receiverid=sender.id).update(receiver_delete=True)
	Letter.objects.filter(sender_delete=True, receiver_delete=True).delete()
	return AjaxSuccess("success!")

	

	
