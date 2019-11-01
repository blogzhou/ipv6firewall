# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import time

from .models import Task

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'task_name', 'start_ip', 'end_ip', 'result', 'add_time']
    readonly_fields = ['result', 'message', 'add_time', 'task_id']

    def save_model(self, request, obj, form, change):
        t = time.time()
        obj.task_id = str(int(t))  # 时间戳
        obj.result = 'create'
        obj.save()


admin.site.register(Task, TaskAdmin)
