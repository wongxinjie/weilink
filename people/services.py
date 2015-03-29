#-*- coding: utf-8 -*-
from django.db.models import Q, Count
from weilink.settings import MESSAGE_EACH_PAGE, TOTAL_MESSAGE_COUNT
from message.models import Message, Comment
from com.utils import paginate
from models import People, Relationship, Blacklist

def get_recent_messages(request):
	user = request.user
	page = request.GET.get("page", "")

	follow_ids = Relationship.objects.filter(followerid=user.id).values_list('wluserid', flat=True)
	follow_ids = list(follow_ids)
	follow_ids.append(user.id)
	message_query = Message.objects.filter(author_id__in=follow_ids).exclude(Q(private=True), ~Q(author_id=user.id))
	query_len = len(message_query)
	if query_len > TOTAL_MESSAGE_COUNT:
		messages = message_query[0:TOTAL_MESSAGE_COUNT]
	else:
		messages = message_query
	return paginate(messages, MESSAGE_EACH_PAGE, page)

def relation_state(authuser, puser):
	follow_query = Relationship.objects.filter(wluserid=puser.id, followerid=authuser.id)
	fan_query = Relationship.objects.filter(wluserid=authuser.id, followerid=puser.id)
	onlist_query = Blacklist.objects.filter(wluserid=puser.id, blackerid=authuser.id)
	putlist_query = Blacklist.objects.filter(wluserid=authuser.id, blackerid=puser.id)

	if onlist_query or putlist_query:
		state = "BLACKLIST"
	else:
		if follow_query and fan_query:
			state = "FRIEND"
		elif follow_query:
			state = "FOLLOW"
		else:
			state = "NOTHING"
	
	return state
	

def friend_state(authuser, puser):
	fan_query = Relationship.objects.filter(wluserid=authuser.id, followerid=puser.id)
	if fan_query:
		return "FRIEND"
	else:
		return "FOLLOW"

def fan_state(authuser, puser):
	follow_query = Relationship.objects.filter(wluserid=puser.id, followerid=authuser.id)
	if follow_query:
		return "FRIEND"
	else:
		return "FAN"


def newuser_recommend():
	follows_dict = Relationship.objects.values('wluserid').annotate(fancount=Count('wluserid'))
	if len(follows_dict) > 11:
		follow_dict = follow_dict[0:10]
	followids = []
	for follow_dict in follows_dict:
		followids.append(follow_dict['wluserid'])
	
	top10_follows = People.objects.filter(user_id__in=followids)
	return top10_follows


	
	

	


	

	


