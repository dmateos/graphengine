# Generated by Django 4.1.6 on 2023-11-15 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("l4mbda", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="storage",
            field=models.TextField(default=""),
        ),
    ]
