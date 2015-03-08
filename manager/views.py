#-*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, RequestContext
from django.contrib.auth.moels import User
from django.contrib.auth import authenticate, login

from DjangoVerifyCode import Code
from weilink.settings import USER_EACH_PAGE, PERMISSION_TO_DELETE_USER, PERMISSION_TO_DELETE_MANAGER
from com.securities import manager_required
from people.models import People
from models import Manager


def manager_login(request):
	if request.method == 'GET':
		return render_to_response("manager/login.html", RequestContext(request))
	
	email = request.POST.get("email", "").strip()
	password = request.POST.get("password", "").strip()
	permisssion = request.POST.get("permission", "").strip()
	verify = request.POST.get("verify", "").strip()
	
	code = Code(request)
	if not code.check(verify):
		return render_to_response("manager/login.html", {"verify_error": True}, RequestContext(request))
	
	user = authenticate(username=email, password=password)
	if user and user.is_staff and user.is_active:
		login(request, user)
		return HttpResponseRedirect("/manager")
	else:
		return render_to_response("manager/login.html", {"account_error": True}, RequestContext(request))


@manager_required
def create_manager(request):
	if request.method == 'GET':
		return render_to_response("manager/create.html", RequestContext(request))
	
	authuser=request.user
	authmanager = authuser.manager
	name = request.POST.get("name", "").strip()
	login_email = request.POST.get("lemail", "").strip()
	password = request.POST.get("password", "").strip()
	contact_email = request.POST.get("cemail", "").strip()
	permission = request.POST.get("permission", "").strip()
	
	error_msg = {}
	if not name:
		error_msg['name_error'] = True
	if not login_email:
		error_msg['lemail_error'] = True
	if not password:
		error_msg['password'] = True
	if not contact_email:
		error_msg['cemail_error'] = True
	
	if not( permission and permission.isdigit()):
		error_msg['permission_error'] = True
	else:
		permission = int(permission)
		if permission <= authmanager.permission:
			error_msg['permission_error'] = True
	
	if not error_msg:
		return render_to_response("manager/create.html", error_msg, RequestContext(request))
	
	user = User.objects.create_user(username=login_email, email=login_email, password=password)
	user.is_staff = True
	user.save()
	
	manager = Manager()
	manager.user = user
	manager.name = name
	manager.contact_email = contact_email
	manager.permission = permission
	manager.save()	
	return HttpResponseRedirect("/manager/mlist")


@manager_required
def list_manager(request):
	authuser = request.user
	authmanager = authuser.manager
	manager_list = Manager.objects.filter(permission__lte=authmanager.permission)
	return render_to_response("manager/mlist.html", {"manager_list": manager_list}, RequestContext(request))


@manager_required
def list_user(request):
	peoples = People.objects.all()
	page = request.GET.get("page", "")
	people_list = paginate(peoples, USER_EACH_PAGE, page)
	return render_to_response("manager/ulist.html", {"people_list": people_list}, RequestContext(request))


@manager_required
def band_user(request, pid):
	people = get_object_or_404(People, pk=pid)
	puser = people.user
	if puser.is_active:
		puser.is_active = False
		puser.save()
	else:
		puser.is_active = True
		puser.save()
	return AjaxSuccess("success!")


@manager_required
def band_manager(request, mid):
	authmanager = request.user.manager
	manager = get_object_or_404(Manager, pk=mid)

	if manager.permission <= authmanager.permission:
		return AjaxAlert("permission deny!")
	
	muser = manager.user
	if muser.is_active:
		muser.is_active = False
		muser.save()
	else:
		muser.is_active = True
		muser.save()
	return AjaxSuccess("success!")


@manager_required
def remove_manager(request, mid):
	manager = get_object_or_404(Manager, pk=pid)
	muser = manager.user
	
	authm = request.user.manager
	if authm.permission > PERMISSION_TO_DELETE_MANAGER:
		return HttpResponseRedirect("/manager/mlist")
	
	manager.delete()
	muser.delete()
	
	return HttpResponse("/manager/mlist")


	
