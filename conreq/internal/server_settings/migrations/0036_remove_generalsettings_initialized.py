# Generated by Django 4.0 on 2021-12-20 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0035_remove_stylingsettings_initialized"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="generalsettings",
            name="initialized",
        ),
    ]
