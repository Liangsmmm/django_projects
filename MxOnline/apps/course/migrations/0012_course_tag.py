# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-29 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0011_course_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='\u8bfe\u7a0b\u6807\u7b7e'),
        ),
    ]