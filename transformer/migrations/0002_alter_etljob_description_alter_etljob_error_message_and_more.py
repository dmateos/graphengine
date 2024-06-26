# Generated by Django 4.1.6 on 2024-04-03 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transformer", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="etljob",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="etljob",
            name="error_message",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="etljob",
            name="status",
            field=models.CharField(
                choices=[
                    ("CREATED", "CREATED"),
                    ("PENDING", "PENDING"),
                    ("RUNNING", "RUNNING"),
                    ("SUCCESS", "SUCCESS"),
                    ("FAILED", "FAILED"),
                    ("ERROR", "ERROR"),
                ],
                default="CREATED",
                max_length=100,
            ),
        ),
    ]
