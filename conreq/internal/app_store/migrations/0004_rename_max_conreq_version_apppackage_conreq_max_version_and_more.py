# Generated by Django 4.0 on 2021-12-15 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_store", "0003_rename_description_apppackage_short_description_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="apppackage",
            old_name="max_conreq_version",
            new_name="conreq_max_version",
        ),
        migrations.RenameField(
            model_name="apppackage",
            old_name="minimum_conreq_version",
            new_name="conreq_minimum_version",
        ),
        migrations.RenameField(
            model_name="apppackage",
            old_name="tested_conreq_version",
            new_name="conreq_tested_version",
        ),
    ]
