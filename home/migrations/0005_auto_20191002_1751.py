# Generated by Django 2.1.1 on 2019-10-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_auto_20191002_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stgdisagregationcategory',
            name='name',
            field=models.CharField(default='Not Applicable', max_length=230),
        ),
        migrations.AlterField(
            model_name='stgdisagregationoptions',
            name='name',
            field=models.CharField(default='Not Applicable', max_length=230),
        ),
        migrations.AlterField(
            model_name='stgvaluedatatype',
            name='name',
            field=models.CharField(default='Not Applicable', max_length=50, verbose_name='Value Type'),
        ),
    ]
