# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-27 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_category_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category',
            field=models.CharField(default='category', max_length=30),
        ),
    ]
