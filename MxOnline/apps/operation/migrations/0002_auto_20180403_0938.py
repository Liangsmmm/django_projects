# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-03 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='user',
            field=models.IntegerField(default=0, verbose_name='\u63a5\u6536\u7528\u6237'),
        ),
    ]
