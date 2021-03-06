# Generated by Django 4.0.2 on 2022-03-19 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_mgt', '0002_remove_internetclient_verified_internetclient_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internetclient',
            name='address',
            field=models.CharField(max_length=255, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='internetclient',
            name='city',
            field=models.CharField(max_length=100, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='internetclient',
            name='dob',
            field=models.DateField(null=True, verbose_name='date_of_birth'),
        ),
        migrations.AlterField(
            model_name='internetclient',
            name='gender',
            field=models.CharField(choices=[('agender', 'Agender'), ('androgyne', 'Androgyne'), ('gender_fluid', 'Gender Fluid'), ('male', 'Male'), ('non_binary', 'Non Binary'), ('transgender', 'Transgender'), ('female', 'Female')], max_length=50, null=True, verbose_name='gender'),
        ),
        migrations.AlterField(
            model_name='internetclient',
            name='postal_code',
            field=models.CharField(max_length=20, null=True, verbose_name='postal_code'),
        ),
    ]
