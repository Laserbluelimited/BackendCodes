# Generated by Django 4.0.2 on 2022-03-28 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_mail', '0003_alter_e_mail_body_html_alter_e_mail_body_txt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e_mail',
            name='body_txt',
            field=models.TextField(verbose_name='body_txt'),
        ),
    ]
