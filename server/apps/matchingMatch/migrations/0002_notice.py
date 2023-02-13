# Generated by Django 4.1.5 on 2023-02-13 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchingMatch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('writer', models.CharField(max_length=32)),
                ('content', models.TextField()),
                ('hits', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
