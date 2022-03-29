# Generated by Django 4.0.2 on 2022-03-25 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('payment_id', models.CharField(max_length=20, verbose_name='payment_id')),
                ('medium', models.CharField(default='stripe', max_length=20, verbose_name='medium')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('stripe_session_id', models.CharField(max_length=255, verbose_name='stripe_sess_id')),
            ],
        ),
    ]
