# Generated by Django 2.1.2 on 2020-09-30 16:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0002_auto_20200930_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgeconomiczones',
            name='date_lastupdated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Modified'),
        ),
        migrations.AlterField(
            model_name='stglocation',
            name='date_lastupdated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Modified'),
        ),
        migrations.AlterField(
            model_name='stglocationlevel',
            name='date_lastupdated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date Modified'),
        ),
    ]