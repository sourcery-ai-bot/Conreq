# Generated by Django 4.1.4 on 2022-12-08 03:39

import multiselectfield.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app_store", "0029_appnoticemessage_alter_apppackage_banner_message_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apppackage",
            name="sys_platforms",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("Any", "Any"),
                    ("Linux", "Linux"),
                    ("Windows", "Windows"),
                    ("Darwin", "MacOS"),
                    ("FreeBSD", "FreeBSD"),
                ],
                default="Any",
                max_length=40,
                verbose_name="Supported Platforms",
            ),
        ),
    ]
