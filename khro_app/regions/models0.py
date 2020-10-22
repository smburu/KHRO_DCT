import datetime
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from khro_app.home.models import (StgDisagoptionCombination, StgDatasource,
    StgMeasuremethod, StgValueDatatype,StgPeriodType)
from khro_app.regions.models import StgLocation
from khro_app.common_info.models import CommonInfo

import decimal

STATUS_CHOICES = ( #choices for approval of indicator data by authorized users
    ('pending', 'Pending'),
    ('approved','Approved'),
    ('rejected','Rejected'),
)

PUBLIC_ACCESS = ( #choices for results chain defined by WHO framework of actionn
    ('false', 'False'),
    ('true','True'),
)

def make_choices(values):
    return [(v, v) for v in values]


class StgIndicatorReference(CommonInfo):
    reference_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False, null=False,
        verbose_name = 'Reference Name')  # Field name made lowercase.
    shortname = models.CharField(max_length=50, blank=True, null=True,
        verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField( blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_indicator_reference'
        verbose_name = 'Reference'
        verbose_name_plural = 'Indicator References'
        ordering = ('code', )

    def __str__(self):
        return self.name #display the data source name


class StgIndicator(CommonInfo):

    FRAMEWORK_LEVEL = ( #choices for results chain defined by WHO framework of actionn
        ('', 'Not  Specified'),
        ('input', 'Health input'),
        ('output','Health Output '),
        ('outcome','Health Outcome'),
        ('impact','Health Status'),
    )

    indicator_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField( max_length=500, blank=False, null=False,
        verbose_name = 'Indicator Name')  # Field name made lowercase.
    shortname = models.CharField(unique=True, max_length=120, blank=False,
        null=True, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField( max_length=10, blank=True, null=True,
        verbose_name = 'KHRO Code')  # Field name made lowercase.
    hiscode = models.CharField(max_length=10,blank=True, null=False,
        verbose_name = 'HIS-M&E Code',)  # Field name made lowercase.
    afrocode = models.CharField(max_length=10,blank=True, null=False,
        verbose_name = 'KHIS ID',)  # Field name made lowercase.
    definition = models.TextField(blank=False, null=True,
        verbose_name = 'Indicator Definition')  # Field name made lowercase.
    measuremethod = models.ForeignKey(StgMeasuremethod,
        models.PROTECT,blank=False,
        null=False, default=1,verbose_name = 'Unit of Measure',)
    frame_level = models.CharField(max_length=50,choices= FRAMEWORK_LEVEL,
        null=True,default=FRAMEWORK_LEVEL[0][0], verbose_name='Framework Level')
    numerator_description = models.TextField(blank=True,
        null=True, verbose_name = 'Numerator Description')
    denominator_description = models.TextField(blank=True,null=True,
        verbose_name = 'Denominator Description')  # Field name made lowercase.
    data_sources = models.CharField(max_length=500,blank=True, null=True,
        verbose_name = 'Primary Data Source')
    reference = models.ForeignKey(StgIndicatorReference, models.PROTECT,
        default=1, verbose_name ='Indicator Reference')  # Field name made lowercase.
    periodicity = models.ForeignKey(StgPeriodType, models.PROTECT,
        verbose_name ='Frequency/Periodicity')  # Field name made lowercase.
    public_access = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'stg_indicator'
        verbose_name = 'Indicator'
        verbose_name_plural = '  Indicators'
        ordering = ('name',)
        unique_together = ('code','hiscode','afrocode')

    def __str__(self):
        return self.name #display the indicator name

    # This function makes sure the indicator name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgIndicator.objects.filter(name=self.name).count() and not self.indicator_id:
            raise ValidationError({'name':_('Sorry!Indicator with this  name exists')})

    def save(self, *args, **kwargs):
        super(StgIndicator, self).save(*args, **kwargs)

class StgIndicatorDomain(CommonInfo):
    LEVEL = (1, 2, 3, 4, 5,)

    domain_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=150, blank=False, null=False,
        verbose_name = 'Domain Name')  # Field name made lowercase.
    shortname = models.CharField(max_length=45, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=45, blank=True, null=True,
        verbose_name = 'Domain Code')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True,)  # Field name made lowercase.
    parent = models.ForeignKey('self', models.PROTECT, blank=True, null=True,
        verbose_name = 'Parent Domain')  # Field name made lowercase.
    level = models.IntegerField(choices=make_choices(LEVEL),default=LEVEL[0],
        verbose_name='Level',)
    public_access = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True,blank=True,verbose_name='Sort Order',)
    # this field establishes a many-to-many relationship with the domain table
    indicator = models.ManyToManyField(StgIndicator,db_table='link_indicator_members',
        blank=True,verbose_name = 'Assign Indicators')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_indicator_domain'
        verbose_name = 'Indicator Domain'
        verbose_name_plural = 'Indicator Domains'
        ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay disagregation options

    # This function makes sure a domain name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgIndicatorDomain.objects.filter(name=self.name).count() and not self.domain_id:
            raise ValidationError({'name':_('Sorry! Domain with this name exists')})

    def save(self, *args, **kwargs):
        super(StgIndicatorDomain, self).save(*args, **kwargs)


class FactDataIndicator(CommonInfo):
    fact_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    indicator = models.ForeignKey(StgIndicator, models.PROTECT,blank=False,
        null=False,verbose_name = 'Indicator Name',)  # Field name made lowercase.
    location = models.ForeignKey(StgLocation, models.PROTECT,
        verbose_name = 'Location Name')  # Field name made lowercase.
    categoryoption = models.ForeignKey(StgDisagoptionCombination,
        models.PROTECT,blank=False,verbose_name='Disaggregation Option',
        default=999)  # Field name made lowercase.
    datasource = models.ForeignKey(StgDatasource, models.PROTECT,blank=False,
        null=False, verbose_name = 'Data Source')  # Field name made lowercase.
    # This field is used to lookup the type of data required such as text, integer or float
    measure_type = models.ForeignKey(StgMeasuremethod, models.PROTECT,
        default=2, verbose_name = 'Measure Type')  # Field name made lowercase.
    numerator_value =models.DecimalField(max_digits=20, decimal_places=3,
        blank=True, null=True, verbose_name = 'Numerator')  # Round off the data value based on custom field.
    denominator_value =models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True, verbose_name = 'Denominator')  # Field name made lowercase.
    value_received = models.DecimalField(max_digits=20,decimal_places=3,
        blank=False, null=False, verbose_name = 'Value')  # Field name made lowercase.
    min_value =models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True,verbose_name = 'Minimum Value')  # Field name made lowercase.
    max_value = models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True, verbose_name = 'maximum Value')  # Field name made lowercase.
    target_value = models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True,verbose_name = 'Target Value')  # Field name made lowercase.
    start_period = models.IntegerField(null=False,blank=False,
        verbose_name='Start Year', default=datetime.date.today().year,#extract current date year value only
        help_text="This Year marks the start of the reporting period. NB: 1990 is \
            the Lowest Limit!")
    end_period  = models.IntegerField(null=False,blank=False,
        verbose_name='Ending Year', default=datetime.date.today().year, #extract current date year value only
        help_text="This marks the end of reporting. The value must be current \
            year or greater than the start year")
    period = models.CharField(max_length=25,blank=True,null=False, verbose_name = 'Period') #try to concatenate period field
    status = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], blank=True, null=True,verbose_name='Approval Status')  # Field name made lowercase.
    comment= models.CharField(max_length=5000,blank=True,null=True, verbose_name = 'Comments') # davy's request as of 30/4/2019

    class Meta:
        permissions = (
            ("approve_factdataindicator","Can approve Indicator Data"),
            ("reject_factdataindicator","Can reject Indicator Data"),
            ("pend_factdataindicator","Can pend Indicator Data")
        )

        managed = True
        db_table = 'fact_data_indicator'
        verbose_name = 'Indicator Data'
        verbose_name_plural = '  Columnar Form'
        ordering = ('indicator__name','location__name')
        unique_together = ('indicator', 'location', 'categoryoption','datasource',
            'start_period','end_period',)

    def __str__(self):
         return str(self.indicator)

    """
    The purpose of this method is to compare the start_period to the end_period. If the
    start_period is greater than the end_period athe model should show an inlines error
    message and wait until the user corrects the mistake.
    """

    def clean(self): # Don't allow end_period to be greater than the start_period.
        if self.start_period <=1990 or self.start_period > datetime.date.today().year:
            raise ValidationError({'start_period':_(
                'Sorry! The start year cannot be lower than 1990 or greater than the current Year ')})
        elif self.end_period <=1990 or self.end_period > datetime.date.today().year:
            raise ValidationError({'end_period':_(
                'Sorry! The ending year cannot be lower than the start year or greater than the current Year ')})
        elif self.end_period < self.start_period and self.start_period is not None:
            raise ValidationError({'end_period':_(
                'Sorry! Ending period cannot be lower than the start period. Please make corrections')})

        #This logic ensures that a maximum value is provided for a corresponing minimum value
        if self.min_value is not None and self.min_value !='':
            if self.max_value is None or self.max_value < self.min_value:
                raise ValidationError({'max_value':_(
                    'Data Integrity Problem! You must provide a Maximum that is greater that Minimum value ')})
            elif self.value_received is not None and self.value_received <= self.min_value:
                raise ValidationError({'min_value':_(
                    'Data Integrity Problem! Minimun value cannot be greater that the nominal value')})

    """
    The purpose of this method is to concatenate the date that are entered as start_period and end_period and save
    the concatenated value as a string in the database ---this is very important to take care of Davy's date complexity
    """
    def get_period(self):
        if self.period is None or (self.start_period and self.end_period):
            if self.start_period == self.end_period:
                period = int(self.start_period)
            else:
                period =str(int(self.start_period))+"-"+ str(int(self.end_period))
        return period

    """
    This method overrides the save method to store the derived field into database.
    Note that the last line calls the super class FactDataIndicator to save the value
    """
    def save(self, *args, **kwargs):
        self.period = self.get_period()
        super(FactDataIndicator, self).save(*args, **kwargs)

#this are two proxy classes used to register menu in the admin that will be used to enter tabular inline dat

class IndicatorProxy(StgIndicator):
    """
    Creates permissions for proxy models which are not created automatically by
    'django.contrib.auth.management.create_permissions'.Since we can't rely on
    'get_for_model' we must fallback to 'get_by_natural_key'. However, this
    method doesn't automatically create missing 'ContentType' so we must ensure
    all the models' 'ContentType's are created before running this method.
    We do so by unregistering the 'update_contenttypes' 'post_migrate' signal
    and calling it in here just before doing everything.
    """
    def create_proxy_permissions(app, created_models, verbosity, **kwargs):
        update_contenttypes(app, created_models, verbosity, **kwargs)
        app_models = models.get_models(app)
        # The permissions we're looking for as (content_type, (codename, name))
        searched_perms = list()
        # The codenames and ctypes that should exist.
        ctypes = set()
        for model in app_models:
            opts = model._meta
            if opts.proxy:
                # Can't use 'get_for_model' here since it doesn't return correct 'ContentType' for proxy models
                # See https://code.djangoproject.com/ticket/17648
                app_label, model = opts.app_label, opts.object_name.lower()
                ctype = ContentType.objects.get_by_natural_key(app_label, model)
                ctypes.add(ctype)
                for perm in _get_all_permissions(opts, ctype):
                    searched_perms.append((ctype, perm))

        # Find all the Permissions that have a content_type for a model we're looking for.
        #We don't need to check for codenames since we already have  a list of the ones we're going to create.
        all_perms = set(Permission.objects.filter(
            content_type__in=ctypes,
        ).values_list(
            "content_type", "codename"
        ))

        objs = [
            Permission(codename=codename, name=name, content_type=ctype)
            for ctype, (codename, name) in searched_perms
            if (ctype.pk, codename) not in all_perms
        ]
        Permission.objects.bulk_create(objs)
        if verbosity >= 2:
            for obj in objs:
                sys.stdout.write("Adding permission '%s'" % obj)
        models.signals.post_migrate.connect(create_proxy_permissions) #replaced post_syncdb with post_migrate
        models.signals.post_migrate.disconnect(update_contenttypes)

    class Meta:
        proxy = True
        managed = True
        verbose_name = 'Tabular Form'
        verbose_name_plural = '   Tabular Forms'


    """
    This clean method was contributed by Daniel Mbugua to resolve the issue
    of parent-child saving issue in the multi-records entry form. My credits
    to Daniel of MSc DCT, UoN-Kenya
    """
    def clean(self): #Appreciation to Daniel M.
        pass

# Create achive table for khro indicator data
class Fact_indicator_archive(CommonInfo):
    fact_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    indicator = models.ForeignKey(StgIndicator, models.PROTECT,blank=False,
        null=False,verbose_name = 'Indicator Name',)  # Field name made lowercase.
    location = models.ForeignKey(StgLocation, models.PROTECT,verbose_name = 'Location Name')  # Field name made lowercase.
    categoryoption = models.ForeignKey(StgDisagoptionCombination,
        models.PROTECT,blank=False,verbose_name = 'Disaggregation', default=999)  # Field name made lowercase.
    # This field is used to lookup sources of data such as routine systems, census and surveys
    datasource = models.ForeignKey(StgDatasource, models.PROTECT,blank=False,
        null=False, verbose_name = 'Data Source')  # Field name made lowercase.
    # This field is used to lookup the type of data required such as text, integer or float
    measure_type = models.ForeignKey(StgMeasuremethod, models.PROTECT,
        default=2, verbose_name = 'Measure Type')  # Field name made lowercase.
    numerator_value =models.DecimalField(max_digits=20, decimal_places=3,
        blank=True, null=True, verbose_name = 'Numerator')  # Round off the data value based on custom field.
    denominator_value =models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True, verbose_name = 'Denominator')  # Field name made lowercase.
    value_received = models.DecimalField(max_digits=20,decimal_places=3,
        blank=False, null=False, verbose_name = 'Value')  # Field name made lowercase.
    min_value =models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True,verbose_name = 'Minimum Value')  # Field name made lowercase.
    max_value = models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True, verbose_name = 'maximum Value')  # Field name made lowercase.
    target_value = models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True,verbose_name = 'Target Value')  # Field name made lowercase.
    start_period = models.IntegerField(null=False,blank=False,
        verbose_name='Start Year', default=datetime.date.today().year,#extract current date year value only
        help_text="This Year marks the start of the reporting period. NB: 1990 is the Lowest Limit!")
    end_period  = models.IntegerField(null=False,blank=False,
        verbose_name='Ending Year', default=datetime.date.today().year, #extract current date year value only
        help_text="This marks the end of reporting. The value must be current year or greater than the start year")
    period = models.CharField(max_length=25,blank=True,null=False, verbose_name = 'Period') #try to concatenate period field
    status = models.CharField(max_length=10, choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], blank=True, null=True,verbose_name='Approval Status')  # Field name made lowercase.
    comment= models.CharField(max_length=5000,blank=True,null=True, verbose_name = 'Comments') # davy's request as of 30/4/2019


    class Meta:
        managed = False
        db_table = 'khro_indicator_archive'
        verbose_name = 'Archive'
        verbose_name_plural = 'Facts Archive'
        ordering = ('indicator__name','location__name')

    def __str__(self):
         return str(self.indicator)


class StgNarrative_Type(CommonInfo):
    type_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField( max_length=500, blank=False, null=False,
        verbose_name = 'Narrative Type')  # Field name made lowercase.
    shortname = models.CharField(unique=True, max_length=120,blank=False,
        null=True, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=50, blank=True,null=False,
        verbose_name = 'Narrative Code')  # Field name made lowercase.
    description = models.TextField(blank=False, null=True,
        verbose_name = 'Description' )  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_narrative_type'
        verbose_name = 'Narrative Type'
        verbose_name_plural = 'Narrative Types'
        ordering = ('name',)

    def __str__(self):
        return self.name #display the knowledge product category name


class StgAnalyticsNarrative(CommonInfo):
    analyticstext_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    narrative_type = models.ForeignKey(StgNarrative_Type,models.PROTECT,
        verbose_name = 'Narrative Type', db_column='narrative_type_id') #db_column='narrative_type_id',
    domain = models.ForeignKey(StgIndicatorDomain,models.PROTECT,  blank=False, null=False,
        verbose_name = 'Indicator Domain',  default = 1)
    location = models.ForeignKey(StgLocation, models.PROTECT, blank=False,
        null=False,verbose_name = 'Location', default = 1)  # Field cannot be deleted without deleting its dependants
    code = models.CharField(unique=True, max_length=50, blank=True, null=False,
        verbose_name = 'Narrative Code')  # Field name made lowercase.
    narrative_text = models.TextField(blank=False, null=False,
        verbose_name= ' Narrative Text')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_analytics_narrative'
        verbose_name = 'Analytics Narrative'
        verbose_name_plural = 'Domain-level Narratives'
        ordering = ('-date_created',) #sorted in descending order by date created

    def __str__(self):
        return self.narrative_text

class StgIndicatorNarrative(CommonInfo):
     indicatornarrative_id = models.AutoField(primary_key=True)  # Field name made lowercase.
     uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
     narrative_type = models.ForeignKey(StgNarrative_Type,models.PROTECT,
        verbose_name = 'Narrative Type',db_column='narrative_type_id') #db_column='narrative_type_id',
     indicator = models.ForeignKey('StgIndicator', models.PROTECT,blank=False,
        null=False,verbose_name = 'Indicator Name',)
     location = models.ForeignKey(StgLocation, models.PROTECT, blank=False,
        null=False,verbose_name = 'Location', default = 1)  # Field cannot be deleted without deleting its dependants
     code = models.CharField(unique=True, max_length=50, blank=True, null=False,
        verbose_name = 'Narrative Code')  # Field name made lowercase.
     narrative_text = models.TextField(blank=False, null=False,
        verbose_name= ' Narrative Text')  # Field name made lowercase.

     class Meta:
         managed = True
         db_table = 'stg_indicator_narrative'
         verbose_name = 'Indicator Narrative'
         verbose_name_plural = 'Indicator-level Narratives'
         ordering = ('-date_created',)

     def __str__(self):
         return self.narrative_text


class StgIndicatorGroup(CommonInfo):
    group_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=False, null=False,
        verbose_name = 'Group Name')  # Field
    shortname = models.CharField(unique=True, max_length=120, blank=False,
        null=False, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=50, blank=True,
        null=False, verbose_name = 'Group Code')  # Field name made lowercase.
    description = models.TextField(blank=False, null=False,
        verbose_name ='Description' )  # Field name made lowercase.
    source_system = models.CharField(max_length=100,blank=True, null=True,
        verbose_name = 'External Source')  # Field name made lowercase.
    public_access = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True,blank=True,verbose_name='Sort Order',)
    indicator = models.ManyToManyField(StgIndicator,
        db_table='stg_indicator_membership', blank=True,)  # many-to-many relationship.

    class Meta:
        managed = True
        db_table = 'stg_indicator_group'
        verbose_name = 'Indicator Group'
        verbose_name_plural = 'Indicator Groups'

    def __str__(self):
        return str(self.name)

    # This method ensures that the indicator name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgIndicatorGroup.objects.filter(
            name=self.name).count() and not self.group_id:
            raise ValidationError({'name':_(
                    'Sorry! Indicator Group with same name already exists')})

    def save(self, *args, **kwargs):
        super(StgIndicatorGroup, self).save(*args, **kwargs)

    def get_indicators(self):
        return "\n".join([str(p.name) for p in self.indicator.all()])

class StgIndicatorSuperGroup(CommonInfo):
    groupset_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=False, null=False,
        verbose_name = 'Group Name')  # Field
    shortname = models.CharField(unique=True, max_length=120, blank=False,
        null=False, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=50, blank=True,
        null=False, verbose_name = 'Group Code')  # Field name made lowercase.
    description = models.TextField(blank=False, null=False,verbose_name ='Description' )  # Field name made lowercase.
    source_system = models.CharField(max_length=100,blank=True, null=True,
        verbose_name = 'External Source')  # Field name made lowercase.
    public_access = models.BooleanField(default=False)
    sort_order = models.IntegerField(null=True,blank=True,verbose_name='Sort Order',)
    indicator_groups = models.ManyToManyField(StgIndicatorGroup,
        db_table='link_indicator_supergroup',blank=True,verbose_name='Indicator Groups',)  # creates a many-to-many relationship.

    class Meta:
        managed = True
        db_table = 'stg_indicator_supergroup'
        verbose_name = 'Indicator Groupset'
        verbose_name_plural = 'Indicator Groupsets'

    def __str__(self):
        return str(self.name)

    # This method ensures that the indicator name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgIndicatorSuperGroup.objects.filter(
            name=self.name).count() and not self.groupset_id:
            raise ValidationError({'name':_(
                'Sorry! Indicator Groupset with same name already exists')})

    def save(self, *args, **kwargs):
        super(StgIndicatorSuperGroup, self).save(*args, **kwargs)
