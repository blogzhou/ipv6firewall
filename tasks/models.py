# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from datetime import datetime

# Create your models here.


class Task(models.Model):
    """
    下发任务管理模块
    """
    task_id = models.CharField(max_length=20, verbose_name=u"任务ID")
    task_name = models.CharField(max_length=50, verbose_name=u"任务名")
    start_ip = models.CharField(max_length=39, verbose_name=u"起始IP")
    end_ip = models.CharField(max_length=39, verbose_name=u"中止IP")
    result = models.CharField(choices=(
        ("true", '检测成功'),
        ("false", '检测失败'),
        ("middle", '正在检测'),
        ("create", '创建任务'),
    ), max_length=5, default='create', verbose_name=u"任务状态")
    message = models.TextField(verbose_name=u"其他信息")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.task_id

