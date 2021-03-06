# Generated by Django 3.2.9 on 2022-01-25 11:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_team", "0003_auto_20210927_1252"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api_user", "0003_auto_20211011_0905"),
        ("api_probation", "0003_auto_20220121_0250"),
    ]

    operations = [
        migrations.AlterField(
            model_name="probation",
            name="team",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="probations",
                to="api_team.team",
            ),
        ),
        migrations.AlterField(
            model_name="probation",
            name="title",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="probations",
                to="api_user.titles",
            ),
        ),
        migrations.AlterField(
            model_name="probationcompetence",
            name="assessor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assessors_probation_competencies",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="probationoverallcomment",
            name="assessor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assessors_probation_comments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
