# Generated by Django 3.2.3 on 2022-02-16 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_slackbot", "0005_auto_20220211_1110"),
    ]

    operations = [
        migrations.AddField(
            model_name="templeaverequest",
            name="reason",
            field=models.TextField(default="Personal issues"),
        ),
    ]
