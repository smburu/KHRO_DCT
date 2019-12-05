from django.db import models
import uuid
from khro_app.common_info.models import CommonInfo
#from indicators.models import StgIndicator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class StgDatasource(CommonInfo):
    SOURCE_TYPE = ( #choices for results chain defined by WHO framework of actionn
        ('NA', 'Not Specified'),
        ('routine', 'Routine'),
        ('survey','Survey ')
    )

    datasource_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False, null=False,verbose_name = 'Data Source')  # Field name made lowercase.
    shortname = models.CharField(max_length=50, blank=True, null=True, verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)  # Field name made lowercase.
    source_type = models.CharField(max_length=50, choices= SOURCE_TYPE, null=True,
        default=SOURCE_TYPE[0][0], verbose_name='Source Type')  # Field name made lowercase
    description = models.TextField( blank=True, null=True)  # Field name made lowercase.
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_datasource'
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the data source name

class StgValueDatatype(CommonInfo):
     valuetype_id = models.AutoField(primary_key=True)  # Field name made lowercase.
     uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
     name = models.CharField(max_length=50, blank=False, null=False,default='Not Applicable',
        verbose_name ='Value Type')  # Field name made lowercase.
     shortname = models.CharField(max_length=50, blank=True, null=True, verbose_name = 'Short Name')  # Field name made lowercase.
     code = models.CharField(unique=True, max_length=50)  # Field name made lowercase.
     description = models.TextField(blank=True, null=True)  # Field name made lowercase.

     class Meta:
         managed = True
         db_table = 'stg_value_datatype'
         verbose_name = 'Value Type'
         verbose_name_plural = 'Value Types'
         ordering = ('name', )

     def __str__(self):
         return self.name #ddisplay disagregation options

class StgMeasuremethod(CommonInfo):
    measuremethod_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False, null=False, verbose_name = 'Unit of Measure')  # Field name made lowercase.
    code = models.CharField(max_length=50, unique=True, blank=True, null=False)  # Field name made lowercase.
    measure_value = models.DecimalField(max_digits=50, decimal_places=0, blank=True, null=True, verbose_name = 'Factor')  # Field name made lowercase.
    description = models.TextField(max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_measuremethod'
        verbose_name = 'Indicator Measure'
        verbose_name_plural = 'Indicator Measures'
        ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay measurement methods

# In DHIS2, this is the smallest item of a category (Male, Female, 0-4Y, 5+)
class StgDisagregationOptions(CommonInfo):
    categoryoption_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False,
        null=False,default='Not Applicable')
    shortname = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_disagregation_options'
        verbose_name = 'Disaggregation'
        verbose_name_plural = 'Disaggregation Options'
        ordering = ('name', )

    def __str__(self):
         return self.name #ddisplay disagregation options


# This is a compilation of similar options for disaggregation (sex=Male,Female)
class StgDisagregationCategory(CommonInfo):
    category_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False, null=False,default='Not Applicable')
    shortname = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    dimension_type = models.CharField(max_length=15, blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    datadimension = models.CharField(max_length=6)
    public_access = models.CharField(max_length=6)
    # this field establishes a many-to-many relationship with the domain table
    category_options = models.ManyToManyField(StgDisagregationOptions,db_table='link_category_disaggregate_options',
        blank=True,verbose_name = 'Disaggregation Options')  # Field name made lowercase.
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_disagregation_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Disaggregation Categories'
        ordering = ('name', )

    def __str__(self):
         return self.name #ddisplay disagregation options

# This is logical combination of categories used on datasets eg Age goups and Sex)
class StgCategoryCombination(CommonInfo):
    categorycombo_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False, null=False, default='Not Applicable')
    shortname = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6)

    # this field establishes a many-to-many relationship with the domain table
    categories = models.ManyToManyField(StgDisagregationCategory,db_table='link_categorycombo_categories',
        blank=True,verbose_name = 'Category Combinations')  # Field name made lowercase.
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_category_combination'
        verbose_name = 'Category Combinations'
        verbose_name_plural = 'Category Combinations'
        ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay measurement methods



#This is option combinations according to string value such as (0-4Y Male, 0-4Y Female)
class StgDisagoptionCombination(CommonInfo):
    disag_optionscombo_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False,
        null=False,default='Not Applicable')
    shortname = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.CharField(max_length=6)

    # this field establishes a many-to-many relationship similar to category combinations
    category_options = models.ManyToManyField(StgDisagregationOptions,
        db_table='link_disagoptioncombo_disagoptions',
        blank=True,verbose_name = 'Disaggregation Combinations')  # Field name made lowercase.
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_disagoption_combination'
        verbose_name = 'Disaggregation Combination'
        verbose_name_plural = 'Disaggregation Combinations'
        ordering = ('name', )

    def __str__(self):
         return self.name #ddisplay disagregation options
