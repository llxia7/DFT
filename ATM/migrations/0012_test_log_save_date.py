# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ATM', '0011_action_map_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_log',
            name='save_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]