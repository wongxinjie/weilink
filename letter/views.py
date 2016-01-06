# -*- coding: utf-8 -*-
from datetime import time
from django.shortcuts import render_to_response, get_object_or_404, RequestContext, redirect, render
from django.utils.encoding import smart_str, smart_unicode
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, RequestContext as TemplateRequestContext

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
    receive_people = get_object_or_404(People, pk=rid)
    # import!
    receiver = receive_people.user
    onblacklist = Blacklist.objects.filter(
        wluserid=receiver.id, blackerid=authuser.id)
    if onblacklist:
        return AjaxAlert("onList")
    letter = Letter()
    letter.senderid = authuser.id
    letter.receiverid = receiver.id
    letter.content = content
    letter.save()
    response_data = {}
    response_data['ret'] = 'success'
    response_data['content'] = letter.content
    response_data['send_time'] = letter.send_time.strftime('%Y-%m-%d %H:%M:%S')
    return AjaxData(response_data)


@login_required(login_url="/login")
def history_letters(request, pid):
    sender = request.user
    people = sender.people
    request_people = get_object_or_404(People, pk=pid)
    receiver = request_people.user

    sletter_qset = Letter.objects.filter(
        senderid=sender.id, receiverid=receiver.id, sender_delete=False)
    rletter_qset = Letter.objects.filter(
        senderid=receiver.id, receiverid=sender.id, receiver_delete=False)

    history_letters = list(sletter_qset)
    history_letters.extend(list(rletter_qset))
    history_letters.sort(key=lambda x: x.send_time)
    return render_to_response("people/chat_page.html", {"people": people, "rpeople": request_people, "letter_list": history_letters}, RequestContext(request))


@login_required(login_url="/login")
def letter_page(request):
    authuser = request.user
    new_letters = Letter.objects.filter(been_read=False)
    letters = Letter.objects.filter(senderid=authuser.id)
    people_list = [letter.get_receiver() for letter in letters]
    return render_to_response("people/letters.html", {"people_list": people_list, "new_letters": new_letters}, RequestContext(request))


@login_required(login_url="/login")
@csrf_exempt
def remove_letters(request, pid):
    sender = request.user
    people = get_object_or_404(People, pk=pid)
    receiver = people.user
    Letter.objects.filter(senderid=sender.id, receiverid=receiver.id).update(
        sender_delete=True)
    Letter.objects.filter(senderid=receiver.id, receiverid=sender.id).update(
        receiver_delete=True)
    Letter.objects.filter(sender_delete=True, receiver_delete=True).delete()
    return AjaxSuccess("success!")


@login_required(login_url="/login")
def chat_page(request, pid):
    authuser = request.user
    people = authuser.people

    request_people = get_object_or_404(People, pk=pid)
    request_user = request_people.user
    black_query = Blacklist.objects.filter(
        wluserid=request_user.id, blackerid=authuser.id)
    if black_query or request_user.id == authuser.id:
        return HttpResponseRedirect("/people/home")

    Letter.objects.filter(senderid=request_user.id,
                          receiverid=authuser.id, been_read=False).update(been_read=True)
    sended_letter_query = Letter.objects.filter(
        senderid=authuser.id, receiverid=request_user.id, sender_delete=False)
    received_letter_query = Letter.objects.filter(
        senderid=request_user.id, receiverid=authuser.id, receiver_delete=False)
    sended_letter_list = list(sended_letter_query)
    received_letter_list = list(received_letter_query)
    sended_letter_list.extend(received_letter_list)
    letter_list = sended_letter_list
    letter_list.sort(key=lambda x: x.send_time, reverse=True)
    if len(letter_list) > 10:
        letter_list = letter_list[0:10]
    letter_list.reverse()
    return render_to_response("people/chat_page.html", {"people": people, "rpeople": request_people, "letter_list": letter_list}, RequestContext(request))


@login_required(login_url="/login")
@csrf_exempt
def get_newest_letter(request):
    authuser = request.user
    sid = request.POST.get("sid", "")
    if not(sid and sid.isdigit()):
        return AjaxWarn("Params Error!")
    sid = int(sid)
    speople = get_object_or_404(People, pk=sid)
    suser = speople.user
    letter_query = Letter.objects.filter(
        senderid=suser.id, receiverid=authuser.id, been_read=False)
    letter_list = list(letter_query)
    letter_query.update(been_read=True)
    template = loader.get_template("people/newest_letter.html")
    context = TemplateRequestContext(request, {"letter_list": letter_list})
    return HttpResponse(template.render(context))
