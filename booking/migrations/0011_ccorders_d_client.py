# Generated by Django 4.0.2 on 2022-05-07 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client_mgt', '0006_rename_crprt_client_internetclient_cor_comp'),
        ('booking', '0010_ccart_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ccorders',
            name='d_client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='client_mgt.internetclient'),
            preserve_default=False,
        ),
    ]
