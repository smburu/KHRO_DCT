# Generated by Django 2.1.1 on 2019-10-02 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgcategorycombination',
            name='name',
            field=models.CharField(default='Not Applicable', max_length=230),
            preserve_default=False,
        ),
    ]
