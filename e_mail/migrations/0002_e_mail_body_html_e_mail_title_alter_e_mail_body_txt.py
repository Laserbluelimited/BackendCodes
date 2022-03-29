# Generated by Django 4.0.2 on 2022-03-28 07:21

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('e_mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='e_mail',
            name='body_html',
            field=tinymce.models.HTMLField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='e_mail',
            name='title',
            field=models.CharField(default=1, max_length=100, verbose_name='title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='e_mail',
            name='body_txt',
            field=models.TextField(verbose_name='body_txt'),
        ),
    ]
