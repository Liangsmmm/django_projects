# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-04 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20180331_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(blank=True, default='\u5168\u56fd\u77e5\u540d', max_length=10, null=True, verbose_name='\u673a\u6784\u6807\u7b7e'),
        ),
    ]
