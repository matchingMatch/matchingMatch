# Generated by Django 4.1.6 on 2023-02-10 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applying_teams',
            old_name='applying_id',
            new_name='applying_team',
        ),
        migrations.RenameField(
            model_name='applying_teams',
            old_name='match_id',
            new_name='match',
        ),
    ]
