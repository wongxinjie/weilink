#-*- coding: utf-8 -*-
import re
import sys
import urllib2

def get_title(url):
	req = urllib2.Request(url)
	req.add_header('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:34.0) Gecko/20100101 Firefox/34.0')
	try:
		url_stream = urllib2.urlopen(req)
		title =u'网页链接'
	except urllib2.URLError:
		title = None

	return title





