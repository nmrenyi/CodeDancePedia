# Generated by Django 3.0.7 on 2020-10-29 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
