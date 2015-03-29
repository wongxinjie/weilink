#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from DjangoVerifyCode import Code 
from settings import MESSAGE_EACH_PAGE, DEFAULT_AVATAR_PATH
from com.utils import AjaxSuccess, AjaxFail, paginate, create_token
from com.mail import send_mail
from people.models import People, WlSettings, PasswordTicket
from message.models import Message
import datetime

def index(request):
	if request.user.is_authenticated():
		user = request.user
		people = user.people
		return HttpResponseRedirect('/people/home')
	else:
		return HttpResponseRedirect("/login")
	

def people_login(request):
	if request.method == 'GET':
		return render_to_response('people/login.html', RequestContext(request))
	newuser = request.POST.get("new", "")
	email = request.POST.get("email", "")
	password = request.POST.get("password", "")
	remember = request.POST.get("remember", "")
	if 'try_time' not in request.session:
		try_time = 1
		request.session['try_time'] = try_time
	else:
		try_time = request.session['try_time']
		try_time += 1
		request.session['try_time'] = try_time
	
	if try_time > 2:
		verify = request.POST.get("verify", "")
		code = Code(request)
		if not code.check(verify):
			return render_to_response("people/login.html", {"verify_error": True, "show_verify": True}, RequestContext(request))
	
	user = authenticate(username=email, password=password)
	if user and user.is_active:
		if user.people.verify_status == 1:
			login(request, user) 
			if not remember:
				request.session.set_expiry(0)
			if newuser:
				return HttpResponseRedirect("/people/fillinfo")
			else:
				return HttpResponseRedirect("/")
		else:
			return render_to_response("people/login.html", {"not_verify_error": True}, RequestContext(request))
	else:
		if try_time == 1:
			return render_to_response("people/login.html", {"account_error": True}, RequestContext(request))
		else:
			return render_to_response("people/login.html", {"account_error": True, "show_verify": True}, RequestContext(request))


def signup(request):
	if request.method == 'GET':
		return render_to_response("people/signup.html", RequestContext(request))
	
	request.session.set_expiry(0)
	email = request.POST.get("email", "").strip()
	password1 = request.POST.get("password1", "").strip()
	password2 = request.POST.get("password2", "").strip()
	verify = request.POST.get("verify", "")
	
	if not email or not password1 or not password2:
		return render_to_response("people/signup.html", {"params_error": True}, RequestContext(request))
	if User.objects.filter(email=email, is_staff=False):
		return render_to_response("people/signup.html", {"email_taken": True}, RequestContext(request))
	
	if password1 != password2:
		return render_to_response("people/signup.html", {"password_error": True}, RequestContext(request))
	
	code = Code(request)
	if not code.check(verify):
		return render_to_response("people/signup.html", {"verify_error": True}, RequestContext(request))
	
	user = User.objects.create_user(username=email, email=email, password=password1)
	user.is_staff = False
	user.save()
	
	people = People()
	people.user = user
	people.nickname = 'wlu'+str(user.id)
	people.gender = "U"
	people.sexual = "U" 
	people.feeling = "U"
	people.avatar = DEFAULT_AVATAR_PATH
	people.birthday = datetime.datetime.now().date()
	people.save()
	people.nickname = 'wlu'+str(people.id)
	people.save()
	wlset = WlSettings()
	wlset.wluser = user
	wlset.save()

	access_token = create_token(user.id, email)
	print access_token 
	ticket = PasswordTicket(wluserid=user.id, access_token=access_token)
	ticket.save()

	#Sending mail!
	url = 'http://www.linkwe.xyz/authemail?uid=%d&token=%s' % (user.id, access_token)
	subject = u'LinkWe注册邮箱验证'
	html = u'<p>感谢您注册LinkWe，请点击以下链接完成注册流程</p><p><a href="%s">%s</a></p>' %(url, url)
	send_mail(email, subject, html)
	email_subfix = email.split('@')[-1]
	email_base_url = 'http://mail.'+email_subfix
	return render_to_response("people/authemail.html", {"email_url": email_base_url})


def create_verifycode(request):
	code = Code(request)
	return code.display()

@csrf_exempt
def match_email(request):
	email = request.POST.get("email", "").strip()
	user_query = User.objects.filter(username=email, is_staff=False)
	if user_query:
		return AjaxFail('邮箱已注册，请直接登录')
	else:
		return AjaxSuccess('success!')

def search(request):
	query = request.GET.get("query", "")
	page = request.GET.get("page", "")

	wlset_query = WlSettings.objects.filter(account_visible=False)
	aiuserids = [ aiuser.id for aiuser in [ wlset.wluser for wlset in wlset_query]]
	wlset_query = WlSettings.objects.filter(tweet_visible=False)
	tiuserids = [ riuser.id for riuser in [ wlset.wluser for wlset in wlset_query]]

	messages = Message.objects.filter(private=False, content__icontains=query).exclude(author_id__in=tiuserids)
	peoples = People.objects.filter(nickname__icontains=query).exclude(user_id__in=aiuserids)
	message_list, paginator = paginate(messages, MESSAGE_EACH_PAGE, page)
	
	if request.user.is_authenticated():
		people = request.user.people
	else:
		people = None
	return render_to_response("people/search.html", {"people": people, "messages": message_list, "peoples": peoples, "paginator": paginator, "query": query}, RequestContext(request))


def auth_email(request):
	uid = request.GET.get("uid", "")
	token = request.GET.get("token", "").strip()

	if not(uid and uid.isdigit()) or not token:
		return render_to_response("people/login.html", {"error_message": True}, RequestContext(request))

	uid = int(uid)
	ticket_query = PasswordTicket.objects.filter(wluserid=uid, access_token=token)
	if ticket_query:
		People.objects.filter(user_id=uid).update(verify_status=1)
		ticket_query.delete()
		return render_to_response("people/login.html", {"success_message": True}, RequestContext(request))
	return render_to_response("people/login.html", {"error_message": True}, RequestContext(request))





	
			

