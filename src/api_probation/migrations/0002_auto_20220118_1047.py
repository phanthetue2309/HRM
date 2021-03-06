# Generated by Django 3.2.3 on 2022-01-18 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_probation", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="evaluationtemplate",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="probationcompetence",
            name="evaluation_template_competence",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="probation_competencies",
                to="api_probation.evaluationtemplatecompetence",
            ),
        ),
        migrations.AlterField(
            model_name="probationcompetence",
            name="evaluation_template_competence_assessor_role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="probation_competencies",
                to="api_probation.evaluationtemplatecompetenceassessorrole",
            ),
        ),
    ]
