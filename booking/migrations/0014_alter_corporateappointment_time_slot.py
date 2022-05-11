# Generated by Django 4.0.2 on 2022-05-11 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0006_scheduledates_slug'),
        ('booking', '0013_icorders_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporateappointment',
            name='time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.timeslots'),
        ),
    ]
