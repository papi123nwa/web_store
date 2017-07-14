# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-14 16:02
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0012_auto_20170210_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='highscore',
        ),
        migrations.AddField(
            model_name='transaction',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='developer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='uploaded_games', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
        migrations.AlterField(
            model_name='game',
            name='title',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]
