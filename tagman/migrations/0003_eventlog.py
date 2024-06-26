# Generated by Django 4.1.6 on 2024-04-14 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tagman", "0002_remove_universaltag_schedule_universaltag_schedules"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventLog",
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
                ("event", models.CharField(max_length=255)),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("machine_name", models.CharField(max_length=255)),
            ],
        ),
    ]
