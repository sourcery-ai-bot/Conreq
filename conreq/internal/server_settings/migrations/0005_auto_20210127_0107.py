# Generated by Django 3.1.5 on 2021-01-27 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0004_auto_20210119_1742"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conreqconfig",
            name="conreq_dark_theme",
            field=models.BooleanField(default=True),
        ),
    ]
