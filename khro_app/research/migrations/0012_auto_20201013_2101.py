# Generated by Django 2.1.2 on 2020-10-13 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0011_auto_20201013_1540'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stgknowledgepipeline',
            old_name='period',
            new_name='year_published',
        ),
    ]
