# Generated by Django 4.0.2 on 2022-03-23 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0004_alter_scheduledates_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scheduledates',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='sche_dates_id'),
        ),
        migrations.AlterField(
            model_name='timeslots',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
