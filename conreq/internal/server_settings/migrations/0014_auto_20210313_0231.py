# Generated by Django 3.1.7 on 2021-03-13 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("server_settings", "0013_conreqconfig_conreq_allow_tv_specials"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_app_logo",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_app_url",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_guest_login",
        ),
        migrations.RemoveField(
            model_name="conreqconfig",
            name="conreq_language",
        ),
    ]
