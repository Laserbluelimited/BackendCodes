# Generated by Django 4.0.2 on 2022-03-31 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_mgt', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clinic',
            name='avail_to_work',
            field=models.BooleanField(default=True, verbose_name='avail_to_work'),
        ),
    ]
