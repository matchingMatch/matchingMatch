# Generated by Django 4.1.5 on 2023-02-09 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchinfo',
            name='end_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='matchinfo',
            name='start_time',
            field=models.TimeField(),
        ),
    ]