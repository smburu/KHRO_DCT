# Generated by Django 2.1.1 on 2019-11-19 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commodities', '0007_auto_20191119_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facthealthcommodities',
            name='issue_date',
            field=models.DateField(blank=True, null=True, verbose_name='Date Issued'),
        ),
    ]
