# Generated by Django 3.0.7 on 2020-10-26 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_doc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]