# Generated by Django 4.1.6 on 2024-04-06 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('k8smanager', '0005_alter_ingress_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingress',
            name='host',
            field=models.CharField(default='None', max_length=255),
            preserve_default=False,
        ),
    ]