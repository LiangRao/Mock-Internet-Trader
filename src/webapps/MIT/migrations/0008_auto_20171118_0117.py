# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-18 01:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MIT', '0007_auto_20171105_0043'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remaining_balance', models.FloatField(blank=True, default=0.0)),
                ('net_worth', models.FloatField(blank=True, default=0.0)),
                ('game', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='MIT.Game')),
            ],
        ),
        migrations.RemoveField(
            model_name='player',
            name='game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='net_worth',
        ),
        migrations.RemoveField(
            model_name='player',
            name='remaining_balance',
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='player',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='MIT.Player'),
        ),
    ]
