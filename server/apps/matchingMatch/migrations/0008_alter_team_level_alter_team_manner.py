# Generated by Django 4.1.5 on 2023-02-10 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0007_merge_20230211_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='level',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='manner',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
