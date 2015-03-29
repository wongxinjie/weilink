#-*- coding: utf-8 -*-
from sae.mail import EmailMessage
from weilink.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS

def send_mail(email, subject, body):
	mail = EmailMessage()
	mail.to = email
	mail.subject = subject
	mail.html = body
	mail.smtp = (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS)
	mail.send()




