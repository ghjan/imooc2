# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-26 11:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default='', verbose_name='访问地址'),
        ),
    ]
