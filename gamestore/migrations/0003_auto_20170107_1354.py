# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-07 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0002_game_game_logo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='game_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_highscore',
            new_name='highscore',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_logo',
            new_name='logo',
        ),
        migrations.RenameField(
            model_name='game',
            old_name='game_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='game',
            name='game_price',
        ),
        migrations.AddField(
            model_name='game',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
            preserve_default=False,
        ),
    ]
