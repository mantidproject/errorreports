# Generated by Django 2.2.13 on 2020-08-13 10:53

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
