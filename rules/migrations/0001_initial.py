# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-02 05:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hosts', '0002_host_add_time'),
        ('firetemplate', '0002_firewalltemplate_template_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuleList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_value', models.CharField(max_length=40, verbose_name='\u6a21\u677f\u503c')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('firewall_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='firetemplate.FirewallTemplate', verbose_name='\u89c4\u5219\u6a21\u677f')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hosts.Host', verbose_name='\u4e3b\u673a')),
            ],
            options={
                'verbose_name': '\u89c4\u5219\u5217\u8868',
                'verbose_name_plural': '\u89c4\u5219\u5217\u8868',
            },
        ),
    ]
