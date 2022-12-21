# Generated by Django 4.1 on 2022-12-21 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('StudentHub', '0008_alter_hubpagedatamodel_date_end'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('contact_phone', models.CharField(max_length=12)),
                ('dev_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField(default='empty')),
                ('date', models.DateTimeField(max_length=255, verbose_name=['%Y-%m-%d %H:%M'])),
                ('contact_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='StudentHub.contacts')),
                ('user_id', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
