# Generated by Django 4.1.5 on 2023-02-10 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0005_merge_20230210_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='match_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='designated_match', to='matchingMatch.matchinfo'),
        ),
        migrations.AlterField(
            model_name='team',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d'),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_logo',
            field=models.ImageField(blank=True, null=True, upload_to='posts/%Y%m%d'),
        ),
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(max_length=20),
        ),
    ]
