#-*- coding: utf-8 -*-
from functools import wraps
from django.http import HttpResponseRedirect

def manager_required(redirect_url="/")
	def decorator(func):
		@wraps(func)
		def wrapper(request, *args, **kwargs):
			authuser = request.user
			if authuser.is_authenticated() and authuser.is_staff:
				return func(request, *args, **kwargs)
			else:
				return HttpResponseRedirect(redirect_url)
		return wrapper
	return decorator

