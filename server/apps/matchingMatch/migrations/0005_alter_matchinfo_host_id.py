# Generated by Django 4.1.5 on 2023-02-07 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0004_alter_team_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchinfo',
            name='host_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host_team', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
