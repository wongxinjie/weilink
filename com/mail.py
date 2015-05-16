#-*- coding: utf-8 -*-
from weilink.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, DEBUG
if DEBUG:
    from sae.mail import EmailMessage
    def send_mail(email, subject, body):
	    mail = EmailMessage()
	    mail.to = email
	    mail.subject = subject
	    mail.html = body
	    mail.smtp = (EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS)
	    mail.send()
else:
    from django.core.mail import send_mail as django_mail
    def send_mail(email, subject, body):
        django_mail(subject, body, EMAIL_HOST_USER, email, fail_silently=False)





