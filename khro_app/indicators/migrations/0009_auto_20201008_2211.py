# Generated by Django 2.1.2 on 2020-10-08 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0008_auto_20201008_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgindicatordomain',
            name='public_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stgindicatorgroup',
            name='public_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='stgindicatorsupergroup',
            name='public_access',
            field=models.BooleanField(default=False),
        ),
    ]