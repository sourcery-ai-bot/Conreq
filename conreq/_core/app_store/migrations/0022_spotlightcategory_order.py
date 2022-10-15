# Generated by Django 4.1.1 on 2022-10-13 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_store", "0021_spotlightcategory_apps"),
    ]

    operations = [
        migrations.AddField(
            model_name="spotlightcategory",
            name="order",
            field=models.PositiveIntegerField(
                db_index=True, default=0, editable=False, verbose_name="order"
            ),
            preserve_default=False,
        ),
    ]
