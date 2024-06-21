# Generated by Django 5.0.6 on 2024-06-21 15:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("llmtale", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="agent",
            name="history",
        ),
        migrations.CreateModel(
            name="History",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                (
                    "agent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="llmtale.agent"
                    ),
                ),
            ],
        ),
    ]
