# Generated by Django 4.0.2 on 2022-03-26 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_alter_appointment_appointment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icorders',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='order_id'),
        ),
    ]