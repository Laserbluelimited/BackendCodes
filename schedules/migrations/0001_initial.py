# Generated by Django 4.0.2 on 2022-03-09 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleDates',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='appointment_date_id')),
                ('start_time', models.DateTimeField(verbose_name='start_time')),
                ('end_time', models.DateTimeField(verbose_name='end_time')),
                ('duration', models.DurationField(verbose_name='duration')),
                ('date', models.DateField(verbose_name='date')),
                ('day_of_week', models.CharField(max_length=10, null=True, verbose_name='day_of_week')),
                ('s_time', models.TimeField(verbose_name='actual_star_time')),
                ('e_time', models.TimeField(verbose_name='actual_end_time')),
            ],
        ),
    ]
