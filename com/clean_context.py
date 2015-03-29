#-*- coding: utf-8 -*-
import re
def clean_data(content):
	decoder = {">":"&gt;", "<":"&lt;"}
	if len(content) == 0:
		return None
	content = re.sub("&", "&amp;", content)
	for key in decoder.keys():
		content=re.sub(key, decoder[key], content)
	return content

def get_original_data(content):
	undecoder = {"&gt;":">", "&lt;":"<"}	
	for key in undecoder.keys():
		content=re.sub(key, undecoder[key], content)
	content = re.sub("&amp;", "&", content)
	return content


			


