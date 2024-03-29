# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-11 06:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ATM', '0003_auto_20160408_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log_Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('P', 'Pass'), ('F', 'Fail')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Test_Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_name', models.CharField(max_length=50, unique=True)),
                ('test_date', models.DateTimeField()),
                ('device', models.CharField(max_length=30)),
                ('stage', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['stage'],
            },
        ),
        migrations.RemoveField(
            model_name='test_result',
            name='sub_flow',
        ),
        migrations.DeleteModel(
            name='Test_Result',
        ),
        migrations.AddField(
            model_name='log_detail',
            name='log_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATM.Test_Log'),
        ),
        migrations.AddField(
            model_name='log_detail',
            name='sub_flow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ATM.Action_Map'),
        ),
    ]
