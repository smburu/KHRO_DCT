# Generated by Django 2.1.1 on 2019-10-05 06:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0002_fact_indicator_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='stgindicatorreference',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, verbose_name='Universal ID'),
        ),
    ]
