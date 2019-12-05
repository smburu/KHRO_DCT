# Generated by Django 2.1.1 on 2019-12-05 18:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('regions', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fact_indicator_archive',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('fact_id', models.AutoField(primary_key=True, serialize=False)),
                ('numerator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Numerator')),
                ('denominator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Denominator')),
                ('value_received', models.DecimalField(blank=True, decimal_places=3, max_digits=20, verbose_name='Value')),
                ('min_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Minimum Value')),
                ('max_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='maximum Value')),
                ('target_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Target Value')),
                ('start_period', models.IntegerField(default=2019, help_text='This marks the start of the reporting period. Lowest is 1990!', verbose_name='Start Year')),
                ('end_period', models.IntegerField(default=2019, help_text='Marks end of reporting Perios. Must be greater than start year', verbose_name='Ending Year')),
                ('period', models.CharField(blank=True, max_length=25, verbose_name='Period')),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, null=True, verbose_name='Approval Status')),
                ('comment', models.CharField(blank=True, max_length=5000, null=True, verbose_name='Comments')),
            ],
            options={
                'verbose_name': 'Archive',
                'verbose_name_plural': 'Repository Archive',
                'db_table': 'khro_indicator_archive',
                'ordering': ('indicator__name', 'location__name'),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FactDataIndicator',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('fact_id', models.AutoField(primary_key=True, serialize=False)),
                ('numerator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Numerator')),
                ('denominator_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Denominator')),
                ('value_received', models.DecimalField(decimal_places=3, max_digits=20, verbose_name='Value')),
                ('min_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Minimum Value')),
                ('max_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='maximum Value')),
                ('target_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Target Value')),
                ('start_period', models.IntegerField(default=2019, help_text='This Year marks the start of the reporting period. NB: 1990 is the Lowest Limit!', verbose_name='Start Year')),
                ('end_period', models.IntegerField(default=2019, help_text='This marks the end of reporting. The value must be current year or greater than the start year', verbose_name='Ending Year')),
                ('period', models.CharField(blank=True, max_length=25, verbose_name='Period')),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, null=True, verbose_name='Approval Status')),
                ('comment', models.CharField(blank=True, max_length=5000, null=True, verbose_name='Comments')),
                ('categoryoption', models.ForeignKey(default=999, on_delete=django.db.models.deletion.PROTECT, to='home.StgDisagoptionCombination', verbose_name='Disaggregation')),
                ('datasource', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.StgDatasource', verbose_name='Data Source')),
            ],
            options={
                'verbose_name': 'Indicator Data',
                'verbose_name_plural': '   Data Form',
                'db_table': 'fact_data_indicator',
                'ordering': ('indicator__name', 'location__name'),
                'permissions': (('approve_factdataindicator', 'Can approve Indicator Data'), ('reject_factdataindicator', 'Can reject Indicator Data'), ('pend_factdataindicator', 'Can pend Indicator Data')),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgAnalyticsNarrative',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('analyticstext_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Narrative Code')),
                ('narrative_text', models.TextField(verbose_name=' Narrative Text')),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Location')),
            ],
            options={
                'verbose_name': 'Analytics Narrative',
                'verbose_name_plural': 'Domain-level Narratives',
                'db_table': 'stg_analytics_narrative',
                'ordering': ('-date_created',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgIndicator',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('indicator_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=500, verbose_name='Indicator Name')),
                ('shortname', models.CharField(max_length=120, null=True, unique=True, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='KHRO Code')),
                ('hiscode', models.CharField(blank=True, max_length=10, verbose_name='HIS-M&E Code')),
                ('afrocode', models.CharField(blank=True, max_length=10, verbose_name='KHIS ID')),
                ('definition', models.TextField(null=True, verbose_name='Indicator Definition')),
                ('frame_level', models.CharField(choices=[('', 'Not  Specified'), ('input', 'Health input'), ('output', 'Health Output '), ('outcome', 'Health Outcome'), ('impact', 'Health Status')], default='', max_length=50, null=True, verbose_name='Framework Level')),
                ('numerator_description', models.TextField(blank=True, null=True, verbose_name='Numerator Description')),
                ('denominator_description', models.TextField(blank=True, null=True, verbose_name='Denominator Description')),
                ('data_sources', models.CharField(blank=True, max_length=500, null=True, verbose_name='Primary Data Source')),
                ('periodicity', models.IntegerField(blank=True, default=999, null=True, verbose_name='Frequency')),
                ('public_access', models.CharField(choices=[('false', 'False'), ('true', 'True')], default='True', max_length=6, verbose_name='Publicly Accessible?')),
                ('measuremethod', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.StgMeasuremethod', verbose_name='Unit of Measure')),
            ],
            options={
                'verbose_name': 'Indicator',
                'verbose_name_plural': 'Indicators',
                'db_table': 'stg_indicator',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgIndicatorDomain',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('domain_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=150, verbose_name='Domain Name')),
                ('shortname', models.CharField(max_length=45, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=45, null=True, unique=True, verbose_name='Domain Code')),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], default=1, verbose_name='Level')),
                ('public_access', models.CharField(choices=[('false', 'False'), ('true', 'True')], default='True', max_length=6, verbose_name='Publicly Accessible?')),
                ('sort_order', models.IntegerField(blank=True, null=True, verbose_name='Sort Order')),
                ('indicator', models.ManyToManyField(blank=True, db_table='link_indicator_members', to='indicators.StgIndicator', verbose_name='Assign Indicators')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicatorDomain', verbose_name='Parent Domain')),
            ],
            options={
                'verbose_name': 'Domain',
                'verbose_name_plural': 'Indicator Domains',
                'db_table': 'stg_indicator_domain',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgIndicatorGroup',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=200, verbose_name='Group Name')),
                ('shortname', models.CharField(max_length=120, unique=True, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Group Code')),
                ('description', models.TextField(verbose_name='Description')),
                ('source_system', models.CharField(blank=True, max_length=100, null=True, verbose_name='External Source')),
                ('public_access', models.CharField(choices=[('false', 'False'), ('true', 'True')], default='True', max_length=6, verbose_name='Publicly Accessible?')),
                ('sort_order', models.IntegerField(blank=True, null=True, verbose_name='Sort Order')),
                ('indicator', models.ManyToManyField(blank=True, db_table='stg_indicator_membership', to='indicators.StgIndicator')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'db_table': 'stg_indicator_group',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgIndicatorNarrative',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('indicatornarrative_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Narrative Code')),
                ('narrative_text', models.TextField(verbose_name=' Narrative Text')),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicator', verbose_name='Indicator Name')),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Location')),
            ],
            options={
                'verbose_name': 'Indicator Narrative',
                'verbose_name_plural': 'Indicator-level Narratives',
                'db_table': 'stg_indicator_narrative',
                'ordering': ('-date_created',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgIndicatorReference',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('reference_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=230, verbose_name='Reference Name')),
                ('shortname', models.CharField(blank=True, max_length=50, null=True, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Reference',
                'verbose_name_plural': 'Indicator References',
                'db_table': 'stg_indicator_reference',
                'ordering': ('code',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgIndicatorSuperGroup',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('groupset_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=200, verbose_name='Group Name')),
                ('shortname', models.CharField(max_length=120, unique=True, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Group Code')),
                ('description', models.TextField(verbose_name='Description')),
                ('source_system', models.CharField(blank=True, max_length=100, null=True, verbose_name='External Source')),
                ('public_access', models.CharField(choices=[('false', 'False'), ('true', 'True')], default='True', max_length=6, verbose_name='Publicly Accessible?')),
                ('sort_order', models.IntegerField(blank=True, null=True, verbose_name='Sort Order')),
                ('indicator_groups', models.ManyToManyField(blank=True, db_table='link_indicator_supergroup', to='indicators.StgIndicatorGroup', verbose_name='Indicator Groups')),
            ],
            options={
                'verbose_name': 'Super Group',
                'verbose_name_plural': 'Super Groups',
                'db_table': 'stg_indicator_supergroup',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgNarrative_Type',
            fields=[
                ('date_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date Modified')),
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=500, verbose_name='Narrative Type')),
                ('shortname', models.CharField(max_length=120, null=True, unique=True, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Narrative Code')),
                ('description', models.TextField(null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Narrative Type',
                'verbose_name_plural': 'Narrative Types',
                'db_table': 'stg_narrative_type',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='stgindicatornarrative',
            name='narrative_type',
            field=models.ForeignKey(db_column='narrative_type_id', on_delete=django.db.models.deletion.PROTECT, to='indicators.StgNarrative_Type', verbose_name='Narrative Type'),
        ),
        migrations.AddField(
            model_name='stgindicator',
            name='reference',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicatorReference', verbose_name='Indicator Reference'),
        ),
        migrations.AddField(
            model_name='stganalyticsnarrative',
            name='narrative_type',
            field=models.ForeignKey(db_column='narrative_type_id', on_delete=django.db.models.deletion.PROTECT, to='indicators.StgNarrative_Type', verbose_name='Narrative Type'),
        ),
        migrations.AddField(
            model_name='factdataindicator',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='indicators.StgIndicator', verbose_name='Indicator Name'),
        ),
        migrations.AddField(
            model_name='factdataindicator',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Location Name'),
        ),
        migrations.AddField(
            model_name='factdataindicator',
            name='measure_type',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='home.StgMeasuremethod', verbose_name='Measure Type'),
        ),
        migrations.CreateModel(
            name='IndicatorProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Tabular Indicator Form',
                'verbose_name_plural': 'Data Grid',
                'managed': True,
                'proxy': True,
                'indexes': [],
            },
            bases=('indicators.stgindicator',),
        ),
        migrations.AlterUniqueTogether(
            name='stgindicator',
            unique_together={('code', 'hiscode', 'afrocode')},
        ),
        migrations.AlterUniqueTogether(
            name='factdataindicator',
            unique_together={('indicator', 'location', 'categoryoption', 'start_period', 'end_period')},
        ),
    ]
