# Generated by Django 2.1.1 on 2019-12-05 16:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('regions', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactDataElement',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('fact_id', models.AutoField(primary_key=True, serialize=False)),
                ('value', models.DecimalField(decimal_places=3, max_digits=20, verbose_name='Value')),
                ('target_value', models.DecimalField(blank=True, decimal_places=3, max_digits=20, null=True, verbose_name='Target Value')),
                ('start_year', models.IntegerField(default=2019, verbose_name='Start Year')),
                ('end_year', models.IntegerField(default=2019, verbose_name='Ending Year')),
                ('period', models.CharField(blank=True, max_length=10, verbose_name='Period')),
                ('comment', models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Approval Status')),
            ],
            options={
                'verbose_name': 'Data Element Value',
                'verbose_name_plural': 'Data Form',
                'db_table': 'fact_data_element',
                'ordering': ('location',),
                'permissions': (('approve_factdataelement', 'Can approve Data Element'), ('reject_factdataelement', 'Can reject Data Element'), ('pend_factdataelement', 'Can pend Data Element')),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgDataElement',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('dataelement_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=230, verbose_name='Name')),
                ('shortname', models.CharField(max_length=50, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=45, unique=True)),
                ('dhis_uid', models.CharField(max_length=50, unique=True, verbose_name='DHIS2 ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('domain_type', models.CharField(choices=[('Aggregate', 'Aggregate'), ('Tracker', 'Tracker'), ('Not Applicable', 'Not Applicable')], default='Not Applicable', max_length=50, null=True)),
                ('dimension_type', models.CharField(blank=True, max_length=50, null=True)),
                ('aggregation_type', models.CharField(choices=[('Sum', 'Sum'), ('Average', 'Average'), ('Count', 'Count'), ('Standard Deviation', 'Standard Deviation'), ('Variance', 'Variance'), ('Min', 'Min'), ('max', 'max'), ('None', 'None')], default='Sum', max_length=45, verbose_name='Data Aggregation')),
                ('source_system', models.CharField(blank=True, max_length=100, null=True)),
                ('public_access', models.CharField(default='false', max_length=6)),
                ('categoryoption', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.StgCategoryCombination', verbose_name='Disaggregation Combination')),
                ('value_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.StgValueDatatype', verbose_name='Value Type')),
            ],
            options={
                'verbose_name': 'Data Element',
                'verbose_name_plural': 'Data Elements',
                'db_table': 'stg_data_element',
                'ordering': ('code',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgDataElementGroup',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('group_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(default=uuid.uuid4, editable=False, max_length=36, unique=True, verbose_name='Universal ID')),
                ('name', models.CharField(max_length=200, verbose_name='Group Name')),
                ('shortname', models.CharField(max_length=120, unique=True, verbose_name='Short Name')),
                ('code', models.CharField(blank=True, max_length=50, unique=True, verbose_name='Group Code')),
                ('description', models.TextField(verbose_name='Description')),
                ('dataelement', models.ManyToManyField(blank=True, db_table='stg_data_element_membership', to='elements.StgDataElement')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Element Groups',
                'db_table': 'stg_data_element_group',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='dataelement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='elements.StgDataElement', verbose_name='Data Element Name'),
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='datasource',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.PROTECT, to='home.StgDatasource', verbose_name='Data Source'),
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation', verbose_name='Location'),
        ),
        migrations.AddField(
            model_name='factdataelement',
            name='valuetype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='home.StgValueDatatype', verbose_name='Data Type'),
        ),
        migrations.CreateModel(
            name='DataElementProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Data Grid',
                'verbose_name_plural': 'Data Grid',
                'proxy': True,
                'indexes': [],
            },
            bases=('elements.stgdataelement',),
        ),
        migrations.AlterUniqueTogether(
            name='factdataelement',
            unique_together={('dataelement', 'location', 'start_year', 'end_year')},
        ),
    ]