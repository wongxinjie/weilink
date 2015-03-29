#-*- coding: utf-8 -*-
def local_uploaded_file(img, path):
	with open(path, 'wb+') as destination:
		for chunk in img.chunks():
			destination.write(chunk)
	return path
