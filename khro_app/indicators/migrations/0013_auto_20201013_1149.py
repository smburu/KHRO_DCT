# Generated by Django 2.1.2 on 2020-10-13 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0012_auto_20201009_0522'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stganalyticsnarrative',
            options={'managed': True, 'ordering': ('-date_created',), 'verbose_name': 'Domain Narrative', 'verbose_name_plural': 'Domain Narratives'},
        ),
        migrations.AlterModelOptions(
            name='stgindicatornarrative',
            options={'managed': True, 'ordering': ('-date_created',), 'verbose_name': 'Indicator Narrative', 'verbose_name_plural': 'Indicator Narratives'},
        ),
        migrations.AddField(
            model_name='stganalyticsnarrative',
            name='end_period',
            field=models.IntegerField(default=2020, help_text='This marks the end of reporting. The value must be current         year or greater than the start year', verbose_name='Ending Year'),
        ),
        migrations.AddField(
            model_name='stganalyticsnarrative',
            name='period',
            field=models.CharField(blank=True, max_length=25, verbose_name='Period'),
        ),
        migrations.AddField(
            model_name='stganalyticsnarrative',
            name='start_period',
            field=models.IntegerField(default=2020, help_text='This Year marks the start of the reporting period.         NB: 1990 is the Lowest Limit!', verbose_name='Start Year'),
        ),
        migrations.AddField(
            model_name='stganalyticsnarrative',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, null=True, verbose_name='Approval Status'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicatorDomain', verbose_name='Domain Name'),
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='narrative_text',
            field=models.TextField(verbose_name='Narrative Text'),
        ),
        migrations.AlterField(
            model_name='stgindicatordomain',
            name='level',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, verbose_name='Domain Level'),
        ),
    ]