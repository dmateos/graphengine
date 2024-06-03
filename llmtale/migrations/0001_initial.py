# Generated by Django 5.0.6 on 2024-06-03 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Agent",
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
                ("name", models.CharField(max_length=100)),
                ("history", models.TextField()),
                ("backstory", models.TextField()),
                ("base_image", models.ImageField(upload_to="agents/")),
            ],
        ),
    ]
