from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime #for handling year part of date filed
from home.models import StgDatasource
from regions.models import StgLocation
from common_info.models import CommonInfo


def make_choices(values):
    return [(v, v) for v in values]

class StgResearchTopic(CommonInfo):
    topic_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230)
    shortname = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100)
    public_access = models.CharField(max_length=6)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_research_topic'
        verbose_name = 'Research Topic'
        verbose_name_plural = 'Research Topics'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the knowledge product category name


class StgKnowledgePipelineType(CommonInfo):
    type_id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=230)
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_knowledge_pipeline_type'
        verbose_name = 'Type'
        verbose_name_plural = 'Pipeline Types'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the knowledge product category name


class StgKnowledgePipeline(CommonInfo):
    product_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    code = models.CharField(unique=True, max_length=50)
    title = models.CharField(max_length=2000)
    description = models.TextField(blank=True, null=True)
    type= models.ForeignKey(StgKnowledgePipelineType, models.PROTECT,)
    location = models.ForeignKey(StgLocation, models.PROTECT,)
    topic = models.ForeignKey(StgResearchTopic, models.PROTECT,)
    public_access = models.CharField(max_length=6)

    class Meta:
        managed = True
        db_table = 'stg_knowledge_pipeline'
        verbose_name = 'Knowledge Pipeline'
        verbose_name_plural = 'Knowledge Pipelines'
        ordering = ('title', )

    def __str__(self):
        return self.title #displays the knowledge pipeline title


class StgDiseaseDomain(CommonInfo):
    domain_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230, blank=True, null=False)
    shortname = models.CharField(max_length=120, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6)
    sort_order = models.SmallIntegerField(blank=True, null=True)
    # this field establishes a many-to-many relationship with the domain table
    pipelines = models.ManyToManyField(StgKnowledgePipeline,
        db_table='link_domain_pipelines',
        blank=True,verbose_name = 'Knowledge Pipelines')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_disease_domain'
        verbose_name = 'Domain'
        verbose_name_plural = ' Research Domains'
        ordering = ('name',)

    def __str__(self):
        return self.name #display the knowledge product category name


class StgResearchThemes(CommonInfo):
    theme_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230, blank=True, null=False)
    shortname = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6)
    sort_order = models.SmallIntegerField(blank=True, null=True)
    # this field establishes a many-to-many relationship with the domain table
    domains = models.ManyToManyField(
        StgDiseaseDomain,db_table='link_disease_domain_members',
        blank=True,verbose_name = 'Disease Domains')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_research_themes'
        verbose_name = 'Theme'
        verbose_name_plural = 'Research Themes'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the knowledge product category name



class StgEthicsCommittee(CommonInfo):
    rec_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230)
    shortname = models.CharField(max_length=50)
    location = models.ForeignKey(StgLocation, models.PROTECT,)
    code = models.CharField(max_length=50)
    license_number = models.CharField(max_length=60, blank=True, null=True)
    authorization = models.CharField(max_length=230, blank=True, null=True)
    latitude = models.DecimalField(max_digits=20, decimal_places=15)
    longitude = models.DecimalField(max_digits=20, decimal_places=15)
    start_date = models.DateField()
    end_date = models.DateField()
    status_note = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_ethics_committee'
        verbose_name = 'Ethics Committee'
        verbose_name_plural = 'Ethics Committees'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the knowledge product category name


class StgResearchProposal(CommonInfo):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    product = models.OneToOneField(StgKnowledgePipeline,on_delete=models.CASCADE,
        primary_key=True,verbose_name = 'Pipeline Number')
    erc = models.ForeignKey(StgEthicsCommittee, models.PROTECT,
        verbose_name = 'ERC Number')
    research_objective = models.CharField(max_length=100, blank=True, null=True)
    principal_researcher = models.CharField(max_length=100, blank=True, null=True)
    research_team = models.CharField(max_length=230, blank=True, null=True)
    num_of_researchers = models.IntegerField()
    affiliate_insititutions = models.IntegerField()
    funding_source = models.CharField(max_length=2083, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    approval_status = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], verbose_name='Approval Status')  # Field name made lowercase
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_research_proposal'
        verbose_name = 'Proposal'
        verbose_name_plural = 'Proposals'
        ordering = ('product_id', )

    def __str__(self):
        return self.principal_researcher #display the knowledge product category name

class StgResearchPublication(CommonInfo):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    product = models.OneToOneField(StgKnowledgePipeline,on_delete=models.CASCADE,
        primary_key=True,verbose_name = 'Pipeline Number')
    main_author = models.CharField(max_length=100)
    co_authors = models.CharField(max_length=230, blank=True,null=True,
        verbose_name = 'Co-Authors')
    author_affiliations = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=100)
    internal_link = models.FileField (upload_to='media/files',
        verbose_name = 'File Link',blank=True, null=True)
    cover_image = models.ImageField(upload_to='media/images',
        verbose_name='Cover Page',blank=True, null=True)
    external_link = models.CharField(max_length=2083,blank=True, null=True)
    quality_level = models.CharField(max_length=100, blank=True, null=True)
    period = models.IntegerField(default=datetime.now().year,
        verbose_name='Year Published')
    sharing_status = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], verbose_name='Sharing Status')  # Field name made lowercase
    sort_order = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_research_publication'
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ('product_id', )

    def __str__(self):
        return self.main_author #display the knowledge product category name
