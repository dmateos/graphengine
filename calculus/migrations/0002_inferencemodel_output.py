# Generated by Django 4.1.6 on 2023-11-13 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculus", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="inferencemodel",
            name="output",
            field=models.TextField(blank=True, null=True),
        ),
    ]
