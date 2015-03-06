#-*- coding: utf-8 -*-
from people.models import People, Relationship, Blacklist
from models import Atuser

def process_content(authuser, content, attype, obid):
	piece_list = content.split()
	at_str_list = [ piece for piece in piece_list if '@' in piece]
	nickname_list = []
	for at_str in at_str_list:
		at_parts = at_str.split('@')
		if len(at_parts) > 1:
			nickname_list.append(at_parts[1])
	
	for nickname in nickname_list:
		try:
			people = People.objects.get(nickname=nickname)
			beatuser = people.user
			blacklist_queryset = Blacklist.objects.filter(wluserid=beatuser.id, blackerid=authuser.id)
			if not blacklist_queryset:
				atuser = Atuser()
				atuser.attype = attype
				if attype == 'M':
					messageid = obid
				else:
					commentid = obid
				atuser.atuserid= authuser.id
				atuser.useratid = beatuser.id
				atuser.save()
		except People.DoesNotExist:
			pass


def process_retweet_content(authuser, content, mid):
	piece_list = content.split(':')
	at_str_list = [ piece for piece in piece_list if '@' in piece]
	nickname_list = []
	for at_str in at_str_list:
		at_parts = at_str.split('@')
		if len(at_parts) > 1:
			nickname_list.append(at_parts[1])
	
	for nickname in nickname_list:
		try:
			people = People.objects.get(nickname=nickname)
			beatuser = people.user
			blacklist_queryset = Blacklist.objects.filter(wluserid=beatuser.id, blackerid=authuser.id)
			if not blacklist_queryset:
				atuser = Atuser()
				atuser.attype = 'M'
				atuser.messageid = mid 
				atuser.atuserid= authuser.id
				atuser.useratid = beatuser.id
				atuser.save()
		except People.DoesNotExist:
			pass

	
	
