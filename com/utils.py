#-*- coding: utf-8 -*-
import json
import time
import hashlib
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(object_list, count_each_page, page):
	paginator = Paginator(object_list, count_each_page)
	try:
		objects = paginator.page(page)
	except PageNotAnInteger:
		objects = paginator.page(1)
	except EmptyPage:
		objects = paginator.page(paginator.num_pages)
	return (objects, paginator) 

def create_token(userid, email):
	string = ''.join([str(userid), email, str(time.time())])
	token = hashlib.md5(string).hexdigest()
	return token

def AjaxData(d):
	response = HttpResponse(json.dumps(d))
	response["Content-Type"] = "application/json; charset=utf-8"
	return response

AjaxJump = lambda nexturl: HttpResponse(json.dumps({"ret": "jump",  "nexturl": nexturl}))
AjaxAlert = lambda msg: HttpResponse(json.dumps({"ret": "alert", "msg": msg}))
AjaxWarn = lambda msg: HttpResponse(json.dumps({"ret": "warn", "msg": msg}))
AjaxSuccess = lambda msg: HttpResponse(json.dumps({"ret": "success", "msg": msg}))
AjaxFail = lambda msg: HttpResponse(json.dumps({"ret": "fail", "msg": msg}))
AjaxReload = lambda msg: HttpResponse(json.dumps({"ret": "reload", "msg": msg}))

