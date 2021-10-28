# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-24 03:31
from __future__ import unicode_literals

from django.db import migrations, models
import new_api.files


class Migration(migrations.Migration):

    dependencies = [
        ('STReport', '0005_auto_20160412_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='st_log',
            name='spike_csv',
            field=models.FileField(blank=True, storage=new_api.files.OverwriteStorage(base_url='/files/stest', location='files/stest'), upload_to=''),
        ),
        migrations.AddField(
            model_name='st_log',
            name='time_csv',
            field=models.FileField(blank=True, storage=new_api.files.OverwriteStorage(base_url='/files/stest', location='files/stest'), upload_to=''),
        ),
    ]
