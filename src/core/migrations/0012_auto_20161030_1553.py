# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-30 15:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20161030_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='/avatars/'),
        ),
    ]
