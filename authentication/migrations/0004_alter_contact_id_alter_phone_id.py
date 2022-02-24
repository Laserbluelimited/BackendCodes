# Generated by Django 4.0.2 on 2022-02-23 21:44

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_contact_id_alter_phone_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.IntegerField(default=1110000, primary_key=True, serialize=False, unique=True, verbose_name='contact_id'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='id',
            field=models.IntegerField(default=authentication.models.phone_id_increment, primary_key=True, serialize=False, unique=True, verbose_name='phone_id'),
        ),
    ]
