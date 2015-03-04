#-*- coding: utf-8 -*-
from models import People, Relationship
from message import Message, Comment

def get_recent_messageids(user):
	follow_ids = Relationship.objects.filter(followerid=user.id).values_list('id', flat=True)
	follow_ids.append(userid)
	messages = Message.objects.filter(author_id__in=follow_ids).order_by('pulish_time')
	message_id_list = messages.values_list('id', flat=True)
	return message_id_list 

	


	

	


