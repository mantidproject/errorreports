# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-01-23 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_added_recovery_files'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='errorreport',
            name='recoveryFile',
        ),
        migrations.AddField(
            model_name='errorreport',
            name='stacktrace',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.DeleteModel(
            name='RecoveryFiles',
        ),
    ]
