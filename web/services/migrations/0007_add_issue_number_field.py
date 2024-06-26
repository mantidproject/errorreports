# Generated by Django 3.2.23 on 2024-03-15 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_extend_stacktrace_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='errorreport',
            name='githubIssueNumber',
            field=models.CharField(blank=True, default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='errorreport',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
