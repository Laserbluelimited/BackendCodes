# Generated by Django 4.0.2 on 2022-05-19 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_activated',
            field=models.BooleanField(default=False, verbose_name='activated'),
        ),
    ]
