# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-14 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rulelist',
            name='template_value',
            field=models.CharField(max_length=1000, verbose_name='\u6a21\u677f\u503c'),
        ),
    ]
