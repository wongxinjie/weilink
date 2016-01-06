# -*- coding: utf-8 -*-
from weilink.settings import EMAIL_HOST_USER
from django.core.mail import send_mail as django_mail


def send_mail(email, subject, body):
    django_mail(subject, body, EMAIL_HOST_USER, [email], fail_silently=False)
