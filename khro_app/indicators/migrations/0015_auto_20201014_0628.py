# Generated by Django 2.1.2 on 2020-10-14 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0014_auto_20201013_1236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stganalyticsnarrative',
            options={'managed': True, 'ordering': ('-date_created',), 'verbose_name': 'Thematic Narrative', 'verbose_name_plural': 'Thematic Narratives'},
        ),
        migrations.RenameField(
            model_name='stganalyticsnarrative',
            old_name='analyticstext_id',
            new_name='narrative_id',
        ),
        migrations.RenameField(
            model_name='stgindicatornarrative',
            old_name='indicatornarrative_id',
            new_name='narrative_id',
        ),
        migrations.AlterField(
            model_name='stganalyticsnarrative',
            name='domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicatorDomain', verbose_name='Theme Name'),
        ),
    ]
