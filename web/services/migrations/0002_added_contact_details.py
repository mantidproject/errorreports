from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserDetails",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(help_text="user provided name", max_length=32),
                ),
                (
                    "email",
                    models.CharField(help_text="user provided email", max_length=32),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="application",
            field=models.CharField(blank=True, default="", max_length=80),
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="exitCode",
            field=models.CharField(blank=True, default="", max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="facility",
            field=models.CharField(blank=True, default="", max_length=32),
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="host",
            field=models.CharField(help_text="md5 version of hostname", max_length=32),
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="mantidSha1",
            field=models.CharField(
                help_text="sha1 for specific mantid version", max_length=40
            ),
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="osReadable",
            field=models.CharField(blank=True, default="", max_length=80),
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="uid",
            field=models.CharField(help_text="md5 version of username", max_length=32),
        ),
        migrations.AlterField(
            model_name="errorreport",
            name="upTime",
            field=models.CharField(default="", max_length=32),
        ),
        migrations.AddField(
            model_name="errorreport",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="services.UserDetails",
            ),
        ),
    ]
