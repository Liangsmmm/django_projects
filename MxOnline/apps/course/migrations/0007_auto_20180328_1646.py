# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-28 16:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20180328_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='org',
            new_name='course_org',
        ),
    ]
