from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime #for handling year part of date filed
from khro_app.home.models import StgDatasource
from khro_app.regions.models import StgLocation
from khro_app.common_info.models import CommonInfo

def make_choices(values):
    return [(v, v) for v in values]
LEVEL = (
    (1, 'Level 1'),
    (2, 'Level 2'),
    (3,'Level 3'),
    (4,'Level 4'),
    (5,'Level 5'),
    (6,'Level 6'),
)

class StgResearchTopic(CommonInfo):
    topic_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230)
    shortname = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100,blank=True, null=True)
    public_access = models.BooleanField(default=False)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_research_topic'
        verbose_name = 'Research Topic'
        verbose_name_plural = 'Research Topics'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the knowledge product category name


    def clean(self):
        if StgResearchTopic.objects.filter(
            name=self.name).count() and not self.topic_id and not self.code:
            raise ValidationError({'name':_('Research topic with the same \
                name exists')})

    def save(self, *args, **kwargs):
        super(StgResearchTopic, self).save(*args, **kwargs)

class StgKnowledgePipelineType(CommonInfo):
    type_id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=36)
    name = models.CharField(max_length=230)
    shortname = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_knowledge_pipeline_type'
        verbose_name = 'Product Type'
        verbose_name_plural = 'Product Types'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the knowledge product category name


    def clean(self):
        if StgKnowledgePipelineType.objects.filter(
            name=self.name).count() and not self.type_id and not self.code:
            raise ValidationError({'name':_('Knowledge Resource type with the \
                same name exists')})

    def save(self, *args, **kwargs):
        super(StgKnowledgePipelineType, self).save(*args, **kwargs)


class StgDiseaseDomain(CommonInfo):
    domain_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230, blank=False, null=False)
    shortname = models.CharField(max_length=120, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    level = models.SmallIntegerField(_('Level'),choices=LEVEL,default=LEVEL[0][0])
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.BooleanField(default=False)
    sort_order = models.SmallIntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'stg_disease_domain'
        verbose_name = 'Disease Domain'
        verbose_name_plural = ' Disease Domains'
        ordering = ('name',)

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgDiseaseDomain.objects.filter(
            name=self.name).count() and not self.domain_id and not self.code:
            raise ValidationError({'name':_('ICD11-based taxonomy with the \
                same name exists')})

    def save(self, *args, **kwargs):
        super(StgDiseaseDomain, self).save(*args, **kwargs)


class StgResearchThemes(CommonInfo):
    theme_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230,blank=False, null=False)
    shortname = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100,blank=True, null=True)
    public_access = models.BooleanField(default=False)
    sort_order = models.SmallIntegerField(blank=True, null=True)
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


    def clean(self):
        if StgResearchThemes.objects.filter(
            name=self.name).count() and not self.theme_id and not self.code:
            raise ValidationError({'name':_('Research theme with the same\
                 name exists')})

    def save(self, *args, **kwargs):
        super(StgResearchThemes, self).save(*args, **kwargs)


class StgEthicsCommittee(CommonInfo):
    rec_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    name = models.CharField(max_length=230,blank=False, null=False)
    shortname = models.CharField(max_length=50)
    location = models.ForeignKey(StgLocation, models.PROTECT,)
    code = models.CharField(max_length=50)
    license_number = models.CharField(max_length=60, blank=True, null=True)
    authorization = models.CharField(max_length=230, blank=True, null=True,
        verbose_name='approving authority')
    latitude = models.DecimalField(max_digits=20, decimal_places=15,
        blank=True, null=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15,
        blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status_note = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.BooleanField(default=False)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_ethics_committee'
        verbose_name = 'Ethics Committee'
        verbose_name_plural = 'Ethics Body'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the knowledge product category name

    def clean(self):
        if StgEthicsCommittee.objects.filter(
            name=self.name).count() and not self.rec_id and not self.code:
            raise ValidationError({'name':_('Ethics committee with the same\
                name exists')})

    def save(self, *args, **kwargs):
        super(StgEthicsCommittee, self).save(*args, **kwargs)


class StgKnowledgePipeline(CommonInfo):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    product_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    code = models.CharField(unique=True, max_length=50)
    title = models.CharField(max_length=2000,verbose_name='Product Title')
    description = models.TextField(blank=True, null=True)
    type= models.ForeignKey(StgKnowledgePipelineType, models.PROTECT,
        verbose_name='Product Type')
    theme = models.ForeignKey(StgResearchThemes, models.PROTECT,
        verbose_name ='Thematic Area')
    location = models.ForeignKey(StgLocation, models.PROTECT,)
    main_author = models.CharField(max_length=100,blank=True, null=True)
    co_authors = models.CharField(max_length=230, blank=True,null=True,
        verbose_name = 'Co-authors')
    author_affiliations = models.TextField(blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    publisher = models.CharField(max_length=100,blank=True, null=True)
    internal_link = models.FileField (max_length=300,upload_to='media/files',
        verbose_name = 'File Link',blank=True, null=True)
    external_link = models.CharField(max_length=2083,blank=True, null=True)
    cover_image = models.ImageField(upload_to='media/images',
        verbose_name='Cover Page',blank=True, null=True)
    quality_level = models.SmallIntegerField(_('Quality level'),choices=LEVEL,
            default=LEVEL[0][0])
    year_published = models.SmallIntegerField(default=datetime.now().year,
        verbose_name='Year Published')
    sharing_status = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], verbose_name='Approval Status')  # Field name made lowercase
    sort_order = models.PositiveSmallIntegerField(blank=True, null=True)
    public_access = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'stg_knowledge_pipeline'
        verbose_name = 'Knowledge Poduct'
        verbose_name_plural = '  Knowledge Poducts'
        ordering = ('title', )

    def __str__(self):
        return self.title #displays the knowledge pipeline title

    def clean(self):
        if StgKnowledgePipeline.objects.filter(
            title=self.title).count() and not self.product_id and not self.code:
            raise ValidationError({'name':_('Knowledge product with the same\
                title exists')})

    def save(self, *args, **kwargs):
        super(StgKnowledgePipeline,self).save(*args, **kwargs)


class StgResearchProposal(CommonInfo):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    product_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    code = models.CharField(unique=True, max_length=50)
    title = models.CharField(max_length=2000,verbose_name='Proposal Title')
    topic= models.ForeignKey(StgResearchTopic, models.PROTECT,
        verbose_name ='Research Topic')
    theme = models.ForeignKey(StgResearchThemes, models.PROTECT,
        verbose_name ='Thematic Area')
    erc = models.ForeignKey(StgEthicsCommittee, models.PROTECT,
        verbose_name ='Ethics Reseach Entity')
    location = models.ForeignKey(StgLocation, models.PROTECT,)
    description = models.TextField(blank=True, null=True)
    main_author = models.CharField(max_length=100,blank=True, null=True)
    co_authors = models.CharField(max_length=230, blank=True,null=True,
        verbose_name = 'Co-authors')
    author_affiliations = models.TextField(blank=True, null=True)
    research_objective = models.CharField(max_length=100, blank=True, null=True)
    principal_researcher = models.CharField(max_length=100, blank=True, null=True)
    research_team = models.CharField(max_length=230, blank=True, null=True)
    num_of_researchers = models.IntegerField()
    affiliate_insititutions = models.TextField(blank=True, null=True)
    funding_source = models.CharField(max_length=2083, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    approval_status = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], verbose_name='Approval Status')  # Field name made lowercase
    sort_order = models.SmallIntegerField(blank=True, null=True)
    domains = models.ManyToManyField(StgDiseaseDomain,
        db_table='link_reseach_diseasedomains',
        blank=True,verbose_name = 'Disease Domains')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_research_proposal'
        verbose_name = 'Research Proposal'
        verbose_name_plural = ' Proposals'
        ordering = ('title', )

    def __str__(self):
        return self.title

    def clean(self):
        if StgResearchProposal.objects.filter(
            title=self.title).count() and not self.product_id and not self.code:
            raise ValidationError({'name':_('Research proposal with the same\
                title exists')})

    def save(self, *args, **kwargs):
        super(StgResearchProposal,self).save(*args, **kwargs)
