# Generated by Django 4.1.6 on 2023-11-12 12:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graph',
            name='points',
        ),
        migrations.AddField(
            model_name='graph',
            name='type',
            field=models.CharField(choices=[('line', 'line'), ('bar', 'bar')], default='line', max_length=16),
        ),
        migrations.AddField(
            model_name='graphpoint',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='graphpoint',
            name='graph',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='graph.graph'),
        ),
        migrations.AddField(
            model_name='graphpoint',
            name='label',
            field=models.CharField(default=0, max_length=8),
        ),
        migrations.AddField(
            model_name='graphpoint',
            name='sequence',
            field=models.IntegerField(default=0),
        ),
    ]
