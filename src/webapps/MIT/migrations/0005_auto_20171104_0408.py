# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-04 04:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIT', '0004_auto_20171104_0400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='description',
            field=models.CharField(blank=True, default=' ', max_length=420),
        ),
    ]
