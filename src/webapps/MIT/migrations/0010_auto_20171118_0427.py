# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIT', '0009_auto_20171118_0425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='order_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_time',
            field=models.DateTimeField(blank=True, default=None),
        ),
    ]