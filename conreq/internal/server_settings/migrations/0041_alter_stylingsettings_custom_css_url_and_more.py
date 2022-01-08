# Generated by Django 4.0.1 on 2022-01-08 01:43

from django.db import migrations

import conreq.utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0040_generalsettings_public_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stylingsettings",
            name="custom_css_url",
            field=conreq.utils.fields.URLOrRelativeURLField(
                blank=True, default="", verbose_name="Custom CSS URL"
            ),
        ),
        migrations.AlterField(
            model_name="stylingsettings",
            name="custom_js_url",
            field=conreq.utils.fields.URLOrRelativeURLField(
                blank=True, default="", verbose_name="Custom JavaScript URL"
            ),
        ),
    ]
