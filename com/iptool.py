#-*- coding: utf-8 -*-
import json
import urllib2

def get_location(ip):
	if ip == '127.0.0.1':
		return None

	url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?ip=%s&format=json" % ip 
	try:
		url_stream = urllib2.urlopen(url)
		return_json = url_stream.read()
		if return_json == -2:
			return None

		info = json.loads(return_json)
		if info['ret'] == 1:
			province = info['province']
			city = info['city']
			address = province+','+city
		else:
			address = None
	except Exception:
		address = None
	return address












