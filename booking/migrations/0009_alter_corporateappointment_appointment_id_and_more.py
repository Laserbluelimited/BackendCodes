# Generated by Django 4.0.2 on 2022-04-25 10:29

import booking.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_alter_corporateappointment_appointment_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporateappointment',
            name='appointment_id',
            field=models.CharField(default=booking.models.increment_capp_id, max_length=20, verbose_name='appointment_id'),
        ),
        migrations.AlterField(
            model_name='corporateappointment',
            name='appointment_no',
            field=models.CharField(default=booking.models.increment_capp_no, max_length=20, verbose_name='appointment_no'),
        ),
    ]
