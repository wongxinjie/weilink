#-*- coding: utf-8 -*-
class SetRemoteAddrFromForwardedFor:
	def process_request(self, request):
		try:
			realip = request.META['HTTP_X_RORWARDED_FOR']
		except KeyError:
			pass
		else:
			realip = realip.split(",")[0]
			request.META['REMOTE_ADDR'] = realip

