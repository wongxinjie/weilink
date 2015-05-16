#-*- coding:utf-8 -*-
import requests
import qiniu

def upload(upload_file, key):
	ACCESS_KEY = ''
	SECRET_KEY = ''
	bucket_name = 'staticfiles'
	auth = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
	token = auth.upload_token(bucket_name)
	ret, info = qiniu.put_data(token, key, upload_file)
	if ret is not None:
		return 'SUCCESS'
	else:
		print info
		return 'FAIL'


def remove(avatar_url):
	ACCESS_KEY = ''
	SECRET_KEY = ''
	bucket_name = 'staticfiles'
	auth = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
	bucket = qiniu.BucketManager(auth)
	ret, info = bucket.delete(bucket_name, avatar_url)
	if ret is not None:
		return 'SUCCESS'
	else:
		print info
		return 'FAIL'

