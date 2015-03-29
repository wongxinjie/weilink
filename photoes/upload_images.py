#-*- coding:utf-8 -*-
import requests
import qiniu

def upload(upload_file, key):
	ACCESS_KEY = 'xxxxxx'
	SECRET_KEY = 'xxxxx'
	bucket_name = 'xxxxx'
	auth = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
	token = auth.upload_token(bucket_name)
	ret, info = qiniu.put_data(token, key, upload_file)
	if ret is not None:
		return 'SUCCESS'
	else:
		print info
		return 'FAIL'


def remove(avatar_url):
	ACCESS_KEY = 'CoX5i_ytX10s4SoYtPMLQ5vB5O3AFVZ41Gl0l_-3'
	SECRET_KEY = 'wR-z4A-DdQF390zzUvmnjWHwwCgWk2yLZaFmJmF2'
	bucket_name = 'staticfiles'
	auth = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
	bucket = qiniu.BucketManager(auth)
	ret, info = bucket.delete(bucket_name, avatar_url)
	if ret is not None:
		return 'SUCCESS'
	else:
		print info
		return 'FAIL'

		
