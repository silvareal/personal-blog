# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-02 12:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='User',
            new_name='user',
        ),
    ]