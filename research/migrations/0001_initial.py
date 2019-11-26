# Generated by Django 2.1.1 on 2019-10-02 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('regions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StgDiseaseDomain',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('domain_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=36, unique=True)),
                ('name', models.CharField(blank=True, max_length=230, null=True)),
                ('shortname', models.CharField(blank=True, max_length=120, null=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('source_system', models.CharField(blank=True, max_length=100, null=True)),
                ('public_access', models.CharField(max_length=6)),
                ('sort_order', models.SmallIntegerField(blank=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='research.StgDiseaseDomain')),
            ],
            options={
                'verbose_name': 'Domain',
                'verbose_name_plural': ' Domains (ICD11)',
                'db_table': 'stg_disease_domain',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgEthicsCommittee',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('rec_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=36, unique=True)),
                ('name', models.CharField(max_length=230)),
                ('shortname', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=50)),
                ('license_number', models.CharField(blank=True, max_length=60, null=True)),
                ('authorization', models.CharField(blank=True, max_length=230, null=True)),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status_note', models.TextField(blank=True, null=True)),
                ('source_system', models.CharField(blank=True, max_length=100, null=True)),
                ('public_access', models.CharField(max_length=6)),
                ('sort_order', models.SmallIntegerField(blank=True, null=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation')),
            ],
            options={
                'verbose_name': 'Ethics Committee',
                'verbose_name_plural': 'Ethics Committees',
                'db_table': 'stg_ethics_committee',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgKnowledgePipeline',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=36, unique=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('title', models.CharField(max_length=2000)),
                ('description', models.TextField(blank=True, null=True)),
                ('public_access', models.CharField(max_length=6)),
            ],
            options={
                'verbose_name': 'Pipeline',
                'verbose_name_plural': 'Knowledge Pipelines',
                'db_table': 'stg_knowledge_pipeline',
                'ordering': ('title',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgKnowledgePipelineType',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('type_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=36)),
                ('name', models.CharField(max_length=230)),
                ('code', models.CharField(blank=True, max_length=50, null=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Type',
                'verbose_name_plural': 'Pipeline Types',
                'db_table': 'stg_knowledge_pipeline_type',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgResearchThemes',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('theme_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=36, unique=True)),
                ('name', models.CharField(blank=True, max_length=230, null=True)),
                ('shortname', models.CharField(blank=True, max_length=50, null=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('source_system', models.CharField(blank=True, max_length=100, null=True)),
                ('public_access', models.CharField(max_length=6)),
                ('sort_order', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Theme',
                'verbose_name_plural': 'Thematic Areas',
                'db_table': 'stg_research_themes',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgResearchTopic',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('topic_id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=36, unique=True)),
                ('name', models.CharField(max_length=230)),
                ('shortname', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('source_system', models.CharField(max_length=100)),
                ('public_access', models.CharField(max_length=6)),
                ('sort_order', models.SmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'db_table': 'stg_research_topic',
                'ordering': ('name',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgResearchProposal',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='research.StgKnowledgePipeline', verbose_name='Proposal Number')),
                ('research_objective', models.CharField(blank=True, max_length=100, null=True)),
                ('principal_researcher', models.CharField(blank=True, max_length=100, null=True)),
                ('research_team', models.CharField(blank=True, max_length=230, null=True)),
                ('num_of_researchers', models.IntegerField()),
                ('affiliate_insititutions', models.IntegerField()),
                ('funding_source', models.CharField(blank=True, max_length=2083, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('approval_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Approval Status')),
                ('sort_order', models.SmallIntegerField(blank=True, null=True)),
                ('erc', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='research.StgEthicsCommittee', verbose_name='ERC Number')),
            ],
            options={
                'verbose_name': 'Proposal',
                'verbose_name_plural': 'Proposals',
                'db_table': 'stg_research_proposal',
                'ordering': ('product_id',),
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='StgResearchPublication',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Created')),
                ('date_lastupdated', models.DateTimeField(auto_now=True, null=True, verbose_name='Date Modified')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='research.StgKnowledgePipeline', verbose_name='Publication Number')),
                ('main_author', models.CharField(max_length=100)),
                ('co_authors', models.CharField(blank=True, max_length=230, null=True, verbose_name='Co-Authors')),
                ('author_affiliations', models.TextField(blank=True, null=True)),
                ('abstract', models.TextField(blank=True, null=True)),
                ('publisher', models.CharField(max_length=100)),
                ('internal_link', models.FileField(blank=True, null=True, upload_to='media/files', verbose_name='Attach From File')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='media/images', verbose_name='Attach Cover Image')),
                ('external_link', models.CharField(blank=True, max_length=2083, null=True)),
                ('quality_level', models.CharField(blank=True, max_length=100, null=True)),
                ('period', models.IntegerField(default=2019, verbose_name='Year Published')),
                ('sharing_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10, verbose_name='Sharing Status')),
                ('sort_order', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
                'db_table': 'stg_research_publication',
                'ordering': ('product_id',),
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='stgknowledgepipeline',
            name='domain',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='research.StgDiseaseDomain'),
        ),
        migrations.AddField(
            model_name='stgknowledgepipeline',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='regions.StgLocation'),
        ),
        migrations.AddField(
            model_name='stgknowledgepipeline',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='research.StgResearchTopic'),
        ),
        migrations.AddField(
            model_name='stgknowledgepipeline',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='research.StgKnowledgePipelineType'),
        ),
    ]
