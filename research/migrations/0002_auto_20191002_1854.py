# Generated by Django 2.1.1 on 2019-10-02 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stgdiseasedomain',
            options={'managed': True, 'ordering': ('name',), 'verbose_name': 'Domain', 'verbose_name_plural': ' ICD11-Domains'},
        ),
    ]
