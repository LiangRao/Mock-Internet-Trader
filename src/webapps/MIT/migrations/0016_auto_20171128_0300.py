# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-28 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MIT', '0015_auto_20171125_0404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='interest_rate',
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='ranking',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
