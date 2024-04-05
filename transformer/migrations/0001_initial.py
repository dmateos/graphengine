# Generated by Django 4.1.6 on 2024-04-03 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ETLInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connection_string', models.TextField()),
                ('connection_type', models.CharField(choices=[('FILE_CSV', 'FILE_CSV')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ETLJob',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('RUNNING', 'RUNNING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED'), ('ERROR', 'ERROR')], max_length=100)),
                ('error_message', models.TextField()),
                ('etl_input', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transformer.etlinput')),
            ],
        ),
        migrations.CreateModel(
            name='ETLOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transformer.etljob')),
            ],
        ),
        migrations.AddField(
            model_name='etljob',
            name='etl_output',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transformer.etloutput'),
        ),
    ]