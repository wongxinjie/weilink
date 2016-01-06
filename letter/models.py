# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class Letter(models.Model):
    content = models.CharField(max_length=280, verbose_name=u'内容')
    senderid = models.IntegerField(verbose_name=u'发送者ID')
    receiverid = models.IntegerField(verbose_name=u'接收者ID')
    been_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name=u'发送时间')
    sender_delete = models.BooleanField(default=False, verbose_name=u'发信者删除')
    receiver_delete = models.BooleanField(default=False, verbose_name=u'接收者删除')

    def __unicode__(self):
        return self.content

    def get_receiver(self):
        user = get_object_or_404(User, pk=self.receiverid)
        people = user.people
        return people

    def get_sender(self):
        user = get_object_or_404(User, pk=self.senderid)
        people = user.people
        return people

    class Meta:
        ordering = ['-send_time']
        verbose_name_plural = verbose_name = u'私信'
