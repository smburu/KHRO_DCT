# Generated by Django 2.1.2 on 2020-09-30 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0002_auto_20200102_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fact_indicator_archive',
            options={'managed': False, 'ordering': ('indicator__name', 'location__name'), 'verbose_name': 'Archive', 'verbose_name_plural': 'Repository Archive'},
        ),
        migrations.AlterField(
            model_name='stgindicator',
            name='periodicity',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.StgPeriodType', verbose_name='Frequency/Periodicity'),
        ),
    ]
