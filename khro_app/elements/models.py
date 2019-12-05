from django.db import models
import uuid
import data_wizard #this may be the Godsent solution to data import madness that has refused to go
import datetime
from django.utils import timezone

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from khro_app.regions.models import StgLocation
from khro_app.home.models import (
    StgDatasource, StgCategoryCombination, StgValueDatatype)
from khro_app.common_info.models import CommonInfo

# The following are is a generic functions that serves dropdown list, and proxy permissions
YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]

def make_choices(values):
    return [(v, v) for v in values]

def create_proxy_permissions(app, created_models, verbosity, **kwargs):
    """
    Creates permissions for proxy models which are not created automatically by 'django.contrib.auth.management.create_permissions'.
    Since we can't rely on 'get_for_model' we must fallback to 'get_by_natural_key'. However, this method doesn't automatically create
    missing 'ContentType' so we must ensure all the models' 'ContentType's are created before running this method. We do so by un
    -registering the 'update_contenttypes' 'post_migrate' signal and calling it in here just before doing everything.
    """
    update_contenttypes(app, created_models, verbosity, **kwargs)
    app_models = models.get_models(app)
    # The permissions we're looking for as (content_type, (codename, name))
    searched_perms = list()
    # The codenames and ctypes that should exist.
    ctypes = set()
    for model in app_models:
        opts = model._meta
        if opts.proxy:
            # Can't use 'get_for_model' here since it doesn't return the correct 'ContentType' for proxy models.

            app_label, model = opts.app_label, opts.object_name.lower()
            ctype = ContentType.objects.get_by_natural_key(app_label, model)
            ctypes.add(ctype)
            for perm in _get_all_permissions(opts, ctype):
                searched_perms.append((ctype, perm))

    # Find all the Permissions that have a content_type for a model we're looking for.
    # We don't need to check for codenames since we already have  a list of the ones we're going to create.
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


class StgDataElement(CommonInfo):

    DOMAIN_TYPE = ('Aggregate','Tracker', 'Not Applicable') #domain type concept is inherited from DHIS2

    # These are functions used in systems like DHIS2 to aggregate data based on core dimensions. DHIS2
    # mostly uses Sum and average to aggregate data on period hierarchy-->weekly,monthy,quarterly,annualy
    AGGREGATION_TYPE = ('Sum','Average', 'Count','Standard Deviation', 'Variance', 'Min', 'max','None')

    dataelement_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False, null=False,verbose_name = 'Name')  # Field name made lowercase.
    shortname = models.CharField(max_length=50, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField( unique=True, max_length=45,blank=True, null=False)  # Field name made lowercase.
    dhis_uid = models.CharField(unique=True, max_length=50,verbose_name = 'DHIS2 ID')
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    domain_type = models.CharField(max_length=50, null=True, choices=make_choices(DOMAIN_TYPE),
        default=DOMAIN_TYPE[2])
    dimension_type = models.CharField(max_length=50, blank=True, null=True)
    value_type = models.ForeignKey(StgValueDatatype, models.PROTECT,verbose_name='Value Type')
    categoryoption = models.ForeignKey(StgCategoryCombination, models.PROTECT,
        verbose_name='Disaggregation Combination')
    aggregation_type = models.CharField(max_length=45, choices=make_choices(AGGREGATION_TYPE),
        default=AGGREGATION_TYPE[0],verbose_name = 'Data Aggregation',)  # Field name made lowercase.
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6,default='false')

    class Meta:
        managed = True
        db_table = 'stg_data_element'
        verbose_name = 'Data Element'
        verbose_name_plural = 'Data Elements'
        ordering = ('code',)

    def __str__(self):
        return self.name #display the data element name

    # This function makes sure data elements name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgDataElement.objects.filter(name=self.name).count() and not self.dataelement_id:
            raise ValidationError({'name':_('Sorry! Data element with this name already exists')})
    def save(self, *args, **kwargs):
        super(StgDataElement, self).save(*args, **kwargs)


class FactDataElement(CommonInfo):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    fact_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    dataelement = models.ForeignKey('StgDataElement', models.PROTECT,
        verbose_name = 'Data Element Name')  # Field name made lowercase.
    location = models.ForeignKey(StgLocation, models.PROTECT,verbose_name = 'Location',)  # Field name made lowercase.
    # This field is used to lookup sources of data such as routine systems, census and surveys
    datasource = models.ForeignKey(StgDatasource, models.PROTECT,blank=False,
        null=False,verbose_name = 'Data Source', default = 4)  # Field name made lowercase.
    # This field is used to lookup the type of data required such as text, integer or float
    valuetype = models.ForeignKey(StgValueDatatype, models.PROTECT,
        verbose_name = 'Data Type',  default = 1)  # Field name made lowercase.
    value = models.DecimalField(max_digits=20, decimal_places=3,null=False,
        blank=False, verbose_name = 'Value')  # Field name made lowercase.
    target_value = models.DecimalField(max_digits=20,decimal_places=3,
        blank=True, null=True,verbose_name = 'Target Value')  # Field name made lowercase.
    start_year = models.IntegerField(null=False,blank=False,
        default=datetime.date.today().year,verbose_name='Start Year')
    end_year  = models.IntegerField(null=False,blank=False,
        default=datetime.date.today().year,verbose_name='Ending Year',)
    period = models.CharField(max_length=10,blank=True,
        null=False, verbose_name = 'Period') #try to concatenate period field
    comment = models.CharField(max_length=10,  choices= STATUS_CHOICES,
        default=STATUS_CHOICES[0][0], blank=True,verbose_name='Approval Status')  # Field name made lowercase.

    class Meta:
        permissions = (
            ("approve_factdataelement","Can approve Data Element"),
            ("reject_factdataelement","Can reject Data Element"),
            ("pend_factdataelement","Can pend Data Element")
        )

        managed = True
        db_table = 'fact_data_element'
        verbose_name = 'Data Element Value'
        verbose_name_plural = 'Data Form'
        ordering = ('location', )
        unique_together = ('dataelement', 'location','start_year','end_year')

    def __str__(self):
         return str(self.dataelement)

    """
    The purpose of this method is to compare the start_year to the end_year. If the
    start_year is greater than the end_year athe model should show an inlines error
    message and wait until the user corrects the mistake.
    """
    def clean(self): # Don't allow end_year to be greater than the srart_year.
        if self.start_year <=1990 or self.start_year > datetime.date.today().year:
            raise ValidationError({'start_year':_(
                'Sorry! The start year cannot be lower than 1990 or greater than the current Year ')})
        elif self.end_year <=1990 or self.end_year > datetime.date.today().year:
            raise ValidationError({'end_year':_(
                'Sorry! The end year cannot be lower than start year or greater than the current Year ')})
        elif self.end_year < self.start_year and self.start_year is not None:
            raise ValidationError({'end_year':_(
                'Sorry! Ending year cannot be lower than the start year. Please make corrections')})

    """
    The purpose of this method is to concatenate the date that are entered as start_year
    and end_year and save the concatenated value as a string in the database.
    It is important to take care of Davy's date request
    """
    def get_period(self):
        if self.start_year and self.end_year:
            if self.start_year == self.end_year:
                period = int(self.start_year)
            else:
                period =str(int(self.start_year))+"-"+ str(int(self.end_year))
        return period

    """
    This method overrides the save method to store the derived field into database.
    Note that the last line calls the super class FactDataIndicator to save the value
    """
    def save(self, *args, **kwargs):
        self.period = self.get_period()
        super(FactDataElement, self).save(*args, **kwargs)


class DataElementProxy(StgDataElement): #data elements proxy
    class Meta:
        proxy = True
        verbose_name = 'Data Grid'
        verbose_name_plural = 'Data Grid'

    """
    This def clean (self) method was contributed by Daniel Mbugua to resolve the issue of parent-child
    saving issue in the multi-records entry form. My credits to Mr Mbugua of MSc DCT, UoN-Kenya
    """
    def clean(self):
        pass

class StgDataElementGroup(CommonInfo):
    group_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=200, blank=False, null=False,
        verbose_name = 'Group Name')  # Field
    shortname = models.CharField(unique=True, max_length=120, blank=False,
        null=False, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=50, blank=True,
        null=False, verbose_name = 'Group Code')  # Field name made lowercase.
    description = models.TextField(blank=False, null=False,verbose_name ='Description' )  # Field name made lowercase.
    dataelement = models.ManyToManyField(StgDataElement,
        db_table='stg_data_element_membership',blank=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_data_element_group'
        verbose_name = 'Group'
        verbose_name_plural = 'Element Groups'

    def __str__(self):
        return str(self.name)

    # This method ensures that the indicator name is unique instead of enforcing unque constraint on DB
    def clean(self): # Don't allow end_period to be greater than the start_period.
        if StgDataElementGroup.objects.filter(name=self.name).count() and not self.group_id:
            raise ValidationError({'name':_('Sorry! Data Elements Group with same name already exists')})

    def save(self, *args, **kwargs):
        super(StgDataElementGroup, self).save(*args, **kwargs)
