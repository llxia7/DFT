# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action_Map',
            fields=[
                ('sub_flow', models.CharField(primary_key=True, max_length=30, serialize=False)),
                ('instrument_model', models.CharField(max_length=20)),
                ('action', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['instrument_model'],
            },
        ),
        migrations.CreateModel(
            name='Test_Result',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('device', models.CharField(max_length=30)),
                ('result', models.CharField(max_length=2, choices=[('P', 'Pass'), ('F', 'Fail')])),
                ('test_date', models.DateTimeField()),
                ('stage', models.CharField(max_length=20)),
                ('sub_flow', models.ForeignKey(to='ATM.Action_Map')),
            ],
            options={
                'ordering': ['stage'],
            },
        ),
    ]
