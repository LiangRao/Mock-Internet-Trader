# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-19 06:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MIT', '0011_auto_20171118_0433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_name', models.CharField(max_length=50)),
                ('stock_type', models.CharField(default='INVALID', max_length=20)),
                ('shares', models.IntegerField(default=0)),
                ('total_value', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='limit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='stop',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='overall_gains',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='overall_return',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AddField(
            model_name='gameinfo',
            name='short_reserve',
            field=models.FloatField(blank=True, default=0.0),
        ),
        migrations.AlterField(
            model_name='game',
            name='short',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MIT.Player'),
        ),
        migrations.AddField(
            model_name='stock',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MIT.Game'),
        ),
        migrations.AddField(
            model_name='stock',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MIT.Player'),
        ),
    ]
