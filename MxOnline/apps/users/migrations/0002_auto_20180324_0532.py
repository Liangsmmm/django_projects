# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-24 05:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('male', '\u7537'), ('female', '\u5973')], default='female', max_length=10, verbose_name='\u6027\u522b'),
        ),
    ]
