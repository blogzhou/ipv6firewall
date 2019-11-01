# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import paramiko

from django.contrib import admin

from .models import RuleList
from mission import Mission

# Register your models here.


class RuleListAdmin(admin.ModelAdmin):
    list_display = ['host', 'get_template_name', 'template_value', 'add_time']
    search_fields = ['host__ip', 'host__host_name']
    readonly_fields = ['add_time']

    def get_template_name(self, obj):
        return obj.firewall_template.template_name

    def save_model(self, request, obj, form, change):
        ip = obj.host.ip
        username = obj.host.username
        password = obj.host.password
        rule = obj.firewall_template.config_message
        value = json.loads(obj.template_value)
        command = rule.format(**value)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(ip, 22, username=username, password=password, timeout=10)
            stdin, stdout, stderr = client.exec_command(command)
            print stdin, stdout, stderr
            stdin. stdout, stderr = client.exec_command("firewall-cmd --reload")
            print stdin, stdout, stderr
            stdin, stdout, stderr = client.exec_command("iptables-save")
        except Exception as e:
            print e
        #result = client.readlines()
        #print result
            #print command
            # TODO:下发添加命令
            #Mission().create_firewall_rule(ip, username, password, command)

            obj.save()

    def delete_model(self, request, obj):
        ip = obj.host.ip
        username = obj.host.username
        password = obj.host.password
        rule = obj.firewall_template.config_message
        value = obj.template_value
        # TODO:下发删除命令
        obj.save()


admin.site.register(RuleList, RuleListAdmin)
