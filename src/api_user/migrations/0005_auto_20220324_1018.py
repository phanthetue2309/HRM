# Generated by Django 3.2.3 on 2022-03-24 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_user", "0004_remove_titles_weight"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="title",
        ),
        migrations.AddField(
            model_name="user",
            name="title",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="users", to="api_user.Titles"
            ),
        ),
    ]
