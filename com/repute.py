#-*- coding: utf-8 -*-
from weilink.settings import LOGIN_SCORE, TWEET_SCORE
from people.models import Reputation

def update_reputation(repu, action, location=''):
	if action == 'LOGIN':
		repu.score += LOGIN_SCORE
		repu.level = repu.score/100
		repu.location = location
		repu.save()
	elif action == 'TWEET':
		repu.score += TWEET_SCORE
		repu.level = repu.score/100
		repu.location = location
		repu.save()
	elif action == 'DELETE':
		repu.score -= TWEET_SCORE
		repu.level = repu.score/100
		repu.save()
	else:
		repu.save()

