# Generated by Django 4.0.2 on 2022-03-04 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic_mgt', '0012_appointmentdates_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentdates',
            name='duration',
            field=models.DateTimeField(verbose_name='duration'),
        ),
    ]
