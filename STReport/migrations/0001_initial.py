# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import new_api.files


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ST_log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=60)),
                ('data_log', models.FileField(storage=new_api.files.OverwriteStorage(location='files/stest', base_url='/files/stest'), upload_to='')),
                ('data_csv', models.FileField(storage=new_api.files.OverwriteStorage(location='files/stest', base_url='/files/stest'), upload_to='')),
                ('process_names', models.CharField(max_length=200)),
                ('workstation_model', models.CharField(max_length=10, blank=True)),
                ('workstation_name', models.CharField(max_length=10, blank=True)),
                ('begin_time', models.DateTimeField(max_length=30)),
                ('end_time', models.DateTimeField(max_length=30)),
                ('save_date', models.DateField(auto_now=True)),
                ('tape', models.CharField(max_length=50, blank=True)),
                ('device', models.CharField(max_length=50, blank=True)),
                ('remarks', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='ST_log_attach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('attachment', models.FileField(storage=new_api.files.OverwriteStorage(location='files/stest', base_url='/files/stest'), upload_to='')),
                ('log_pk', models.ForeignKey(to='STReport.ST_log', on_delete=models.CASCADE,)),
            ],
            options={
                'ordering': ['log_pk'],
            },
        ),
    ]
