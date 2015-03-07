#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from DjangoVerifyCode import Code 
from people.models import People

def index(request):
	if request.user.is_authenticated():
		user = request.user
		people = user.people
		return HttpResponseRedirect('/people/home')
	else:
		return HttpResposneRedirect("/login")
	

def login(request):
	if request.method == 'GET':
		return render_to_response('user/login.html', RequestContext(request))
	email = request.POST.get("email", "")
	password = request.POST.get("password", "")
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
			return render_to_response("user/login.html", {"verify_error": True}, RequestContext(request))
	
	user = authenticate(username=email, password=password)
	if user is not None:
		return HttpResponseRedirect("/")
	else:
		return render_to_response("user/login.html", {"account_error": True}, RequestContext(request))


def signup(request):
	if request.method == 'GET':
		return render_to_response("user/signup.html", RequestContext(request))
	
	username = request.POST.get("username", "").strip()
	password1 = reqeust.POST.get("password1", "").strip()
	password2 = request.POST.get("password2", "").strip()
	verify = request.POST.get("verify", "")
	
	if not username or not password1 or not password2:
		return render_to_response("user/signup.html", {"params_error": True}, RequestContext(request))
	
	if password1 != password2:
		return render_to_response("user/signup.html", {"password_error": True}, RequestContext(request))
	
	code = Code(request)
	if not code.check(verify):
		return render_to_response("user/signup.html", {"verify_error": True}, RequestContext(request))
	
	user = User.objects.create_user(username=email, email=email, password=password)
	user.is_staff = False
	user.save()
	people = People()
	people.user = user
	people.nickname = 'wlu'+str(user.id)
	people.gender = "U"
	people.sexual = "U" 
	people.feeling = "U"
	people.save()
	people.nickname = 'wlu'+str(people.id)
	people.save()
	user = authenticate(username=email, password=password)
	return HttpResponseRedirect("/people/fillinfo")

def create_verifycode(request):
	code = Code(request)
	return code.display()



	
			























	
