# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-25 04:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIT', '0013_auto_20171124_0355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_time',
            field=models.DateTimeField(default=None),
        ),
    ]
