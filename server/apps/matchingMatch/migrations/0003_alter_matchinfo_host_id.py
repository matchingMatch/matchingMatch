# Generated by Django 4.1.5 on 2023-02-09 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0002_alter_matchinfo_end_time_alter_matchinfo_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchinfo',
            name='host_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_team', to=settings.AUTH_USER_MODEL),
        ),
    ]
