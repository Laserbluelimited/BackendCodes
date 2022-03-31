# Generated by Django 4.0.2 on 2022-03-31 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_mgt', '0004_alter_internetclient_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='corporateclient',
            name='auth_prsnl_first_name',
        ),
        migrations.RemoveField(
            model_name='corporateclient',
            name='auth_prsnl_last_name',
        ),
        migrations.RemoveField(
            model_name='corporateclient',
            name='auth_prsnl_title',
        ),
        migrations.AddField(
            model_name='corporateclient',
            name='auth_prsnl_name',
            field=models.CharField(max_length=100, null=True, verbose_name='auth_personel_name'),
        ),
        migrations.AddField(
            model_name='corporateclient',
            name='avg_no_order',
            field=models.IntegerField(null=True, verbose_name='avg_no_order'),
        ),
        migrations.AddField(
            model_name='corporateclient',
            name='medium_of_marketing',
            field=models.CharField(max_length=255, null=True, verbose_name='medium_of_marketing'),
        ),
        migrations.AlterField(
            model_name='corporateclient',
            name='pur_system',
            field=models.BooleanField(verbose_name='pur_order_sys'),
        ),
    ]
