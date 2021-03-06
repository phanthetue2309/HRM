# Generated by Django 3.2.3 on 2022-03-01 14:23

import uuid

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_probation", "0009_auto_20220223_1708"),
    ]

    operations = [
        migrations.CreateModel(
            name="EvaluationTemplateType",
            fields=[
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("type_name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "hr_evaluation_template_type",
            },
        ),
        migrations.AddField(
            model_name="evaluationtemplate",
            name="type",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="evaluation_templates",
                to="api_probation.evaluationtemplatetype",
            ),
        ),
    ]
