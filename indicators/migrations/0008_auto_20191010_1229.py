# Generated by Django 2.1.1 on 2019-10-10 09:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0007_stgindicatorsupergroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgindicatorsupergroup',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID'),
        ),
    ]
