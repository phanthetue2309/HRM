# Generated by Django 3.2.9 on 2022-02-16 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_probation", "0006_probation_probation_line_manager"),
    ]

    operations = [
        migrations.AddField(
            model_name="probationreminder",
            name="calendar_id",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
