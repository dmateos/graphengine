# Generated by Django 4.1.6 on 2023-11-13 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("graph", "0002_remove_graph_points_graph_type_graphpoint_created_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="graphpoint",
            name="label",
            field=models.CharField(default=0, max_length=32),
        ),
    ]
