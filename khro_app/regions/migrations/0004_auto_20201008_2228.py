# Generated by Django 2.1.2 on 2020-10-08 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0003_auto_20200930_1910'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stglocation',
            name='public_access',
            field=models.BooleanField(default=False),
        ),
    ]