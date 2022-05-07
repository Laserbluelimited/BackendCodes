# Generated by Django 4.0.2 on 2022-05-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_alter_corporateappointment_appointment_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ccart',
            name='price',
            field=models.IntegerField(default=55, verbose_name='total_price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='corporateappointment',
            name='appointment_no',
            field=models.CharField(max_length=20, verbose_name='appointment_no'),
        ),
    ]
