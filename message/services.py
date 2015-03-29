#-*- coding: utf-8 -*-
import re

from django.shortcuts import get_object_or_404

from people.models import People, Relationship, Blacklist
from message.models import Message
from models import Atuser
from com.hreftool import get_title

def process_content(authuser, content, attype, obid): 
	piece_list = content.split()
	at_str_list = [ piece for piece in piece_list if '@' in piece]
	nickname_list = []
	for at_str in at_str_list:
		at_parts = at_str.split('@')
		if len(at_parts) > 1:
			nickname_list.append(at_parts[1])
	
	exist_accounts = []
	for nickname in nickname_list:
		try:
			people = People.objects.get(nickname=nickname)
			beatuser = people.user
			blacklist_queryset = Blacklist.objects.filter(wluserid=beatuser.id, blackerid=authuser.id)
			if not blacklist_queryset:
				atuser = Atuser()
				atuser.attype = attype
				atuser.objectid = obid
				atuser.atuserid= authuser.id
				atuser.useratid = beatuser.id
				if authuser.id == beatuser.id:
					atuser.benoticed = True
				atuser.save()
			exist_accounts.append((people.id, people.nickname))
		except People.DoesNotExist:
			pass
	
	exist_accounts = list(set(exist_accounts))
	for account in exist_accounts:
		pid, nickname = account 
		original_nickname = '@'+nickname
		new_nickname = '<a href="/people/profile/'+str(pid)+'" class="atlink">@'+nickname+'</a>'
		content = content.replace(original_nickname, new_nickname)
	return content




def process_retweet_content(authuser, content, mid):
	piece_list = content.split(':')
	at_str_list = [ piece for piece in piece_list if '@' in piece]
	nickname_list = []
	for at_str in at_str_list:
		at_parts = at_str.split('@')
		if len(at_parts) > 1:
			nickname_list.append(at_parts[1])

	prevmsg = get_object_or_404(Message, pk=mid)
	if prevmsg.isoriginal:
		nickname_list.append(prevmsg.nickname)
	else:
		if prevmsg.get_original_msg():
			originalauthor = prevmsg.get_original_msg().author
			nickname_list.append(originalauthor.people.nickname)

	exist_accounts = []
	for nickname in nickname_list:
		try:
			people = People.objects.get(nickname=nickname)
			beatuser = people.user
			blacklist_queryset = Blacklist.objects.filter(wluserid=beatuser.id, blackerid=authuser.id)
			if not blacklist_queryset:
				atuser = Atuser()
				atuser.attype = 'M'
				atuser.objectid = mid 
				atuser.atuserid= authuser.id
				atuser.useratid = beatuser.id
				if authuser.id == beatuser.id:
					atuser.benoticed = True
				atuser.save()
			exist_accounts.append((people.id, people.nickname))
		except People.DoesNotExist:
			pass
	exist_accounts = list(set(exist_accounts))
	for account in exist_accounts:
		pid, nickname = account 
		original_nickname = '@'+nickname
		new_nickname = '<a href="/people/profile/'+str(pid)+'" class="atlink">@'+nickname+'</a>'
		content = content.replace(original_nickname, new_nickname)
	return content 
	


def process_content_link(content):
	#compiler = re.compile(r'(http://|https://)(\s+)', re.I)
	compiler = re.compile(r'(http://|https://)(www.|[a-z]{2,4}.)?([A-Za-z0-9]+.)(com|net|io|cn|xyz)(.cn)?(/\S*)?', re.I)
	urls_tuple = compiler.findall(content)
	urls_list = [ ''.join(urls) for urls in urls_tuple ]

	urls_info = []
	for url in urls_list:
		title = get_title(url)
		if title:
			urls_info.append((url, title))

	for url_info in urls_info:
		url, title = url_info
		href = '<a href="'+url+'" class="atlink" title="'+url+'">'+title+'</a>'
		content = content.replace(url, href)
	return content 



	

	
	


