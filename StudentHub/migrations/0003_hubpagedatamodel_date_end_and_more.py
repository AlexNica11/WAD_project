# Generated by Django 4.1 on 2022-10-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentHub', '0002_hubpagedatamodel_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='hubpagedatamodel',
            name='date_end',
            field=models.CharField(default='empty', max_length=255),
        ),
        migrations.AlterField(
            model_name='hubpagedatamodel',
            name='date',
            field=models.CharField(max_length=255),
        ),
    ]
