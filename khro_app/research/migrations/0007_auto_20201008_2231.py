# Generated by Django 2.1.2 on 2020-10-08 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0006_auto_20201008_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgdiseasedomain',
            name='public_access',
            field=models.BooleanField(default=False),
        ),
    ]
