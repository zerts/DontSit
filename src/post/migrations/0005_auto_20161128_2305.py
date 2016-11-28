# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_auto_20161128_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='comments',
        ),
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(to='post.Comment'),
        ),
    ]
