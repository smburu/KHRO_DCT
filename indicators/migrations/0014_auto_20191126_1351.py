# Generated by Django 2.1.1 on 2019-11-26 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0013_auto_20191126_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgindicator',
            name='periodicity',
            field=models.IntegerField(default=999, verbose_name='Frequency'),
        ),
    ]
