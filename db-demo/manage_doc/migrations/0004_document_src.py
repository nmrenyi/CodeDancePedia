# Generated by Django 3.0.7 on 2020-11-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_doc', '0003_document_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='src',
            field=models.IntegerField(choices=[(-1, 'default'), (0, 'upload'), (1, 'cmrc'), (2, 'search.train'), (3, 'zhidao.train'), (4, 'search.dev'), (5, 'zhidao.dev'), (6, 'search.test'), (7, 'zhidao.test')], default=-1),
        ),
    ]