# Generated by Django 4.0.2 on 2022-03-03 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_mgt', '0008_alter_cliniclocation_lat_alter_cliniclocation_long'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliniclocation',
            name='postal_code',
            field=models.CharField(max_length=100, verbose_name='postal_code'),
        ),
    ]
