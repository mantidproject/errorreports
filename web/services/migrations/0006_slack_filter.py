# Generated by Django 2.2.11 on 2020-03-19 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_stacktrace_added_recoveryfile_removed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorreport',
            name='stacktrace',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
