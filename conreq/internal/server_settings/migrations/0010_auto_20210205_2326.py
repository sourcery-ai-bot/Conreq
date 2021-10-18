# Generated by Django 3.1.5 on 2021-02-06 07:26

from django.db import migrations, models

import conreq.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0009_auto_20210204_1938"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conreqconfig",
            name="conreq_app_url",
            field=models.URLField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="conreqconfig",
            name="radarr_url",
            field=conreq.utils.fields.HostnameOrURLField(
                blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="conreqconfig",
            name="sonarr_url",
            field=conreq.utils.fields.HostnameOrURLField(
                blank=True, default=""),
        ),
    ]
