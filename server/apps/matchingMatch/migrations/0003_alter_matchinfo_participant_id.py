# Generated by Django 4.1.6 on 2023-02-09 06:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0002_alter_matchinfo_host_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchinfo',
            name='participant_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant_team', to=settings.AUTH_USER_MODEL),
        ),
    ]
