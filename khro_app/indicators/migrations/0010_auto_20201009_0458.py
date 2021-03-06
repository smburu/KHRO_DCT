# Generated by Django 2.1.2 on 2020-10-09 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0009_auto_20201008_2211'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stgindicatornarrative',
            old_name='narrative_type',
            new_name='type',
        ),
        migrations.AddField(
            model_name='stganalyticsnarrative',
            name='domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicatorDomain', verbose_name='Indicator Domain'),
        ),
    ]
