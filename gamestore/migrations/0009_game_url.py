# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-28 09:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0008_auto_20170124_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='url',
            field=models.URLField(default='null'),
            preserve_default=False,
        ),
    ]
