# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('STReport', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='st_log',
            name='id',
        ),
        migrations.AlterField(
            model_name='st_log',
            name='title',
            field=models.CharField(primary_key=True, max_length=60, serialize=False),
        ),
    ]
