# Generated by Django 2.1.2 on 2020-10-13 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('research', '0012_auto_20201013_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgknowledgepipeline',
            name='year_published',
            field=models.SmallIntegerField(default=2020, verbose_name='Year Published'),
        ),
    ]
