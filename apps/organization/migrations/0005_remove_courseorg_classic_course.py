# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-24 22:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_courseorg_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorg',
            name='classic_course',
        ),
    ]
