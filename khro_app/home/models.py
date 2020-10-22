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

    datasource_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=230, blank=False, null=False,
        verbose_name = 'Data Source')
    shortname = models.CharField(max_length=50, blank=True, null=True,
        verbose_name = 'Short Name')
    code = models.CharField(unique=True, max_length=50, blank=True, null=True)
    source_type = models.CharField(max_length=50, choices= SOURCE_TYPE, null=True,
        default=SOURCE_TYPE[0][0], verbose_name='Source Type')
    description = models.TextField( blank=True, null=True)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_datasource'
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
        ordering = ('name', )

    def __str__(self):
        return self.name #display the data source name

    def clean(self):
        if StgDatasource.objects.filter(
            name=self.name).count() and not self.datasource_id:
            raise ValidationError({'name':_(
                'Sorry! This data source exists')})

    def save(self, *args, **kwargs):
        super(StgValueDatatype, self).save(*args, **kwargs)

class StgValueDatatype(CommonInfo):
     valuetype_id = models.AutoField(primary_key=True)
     uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
     name = models.CharField(max_length=50, blank=False, null=False,
        default='Not Applicable',verbose_name ='Data Type')
     shortname = models.CharField(max_length=50, blank=True, null=True,
        verbose_name = 'Short Name')
     code = models.CharField(unique=True, max_length=50)
     description = models.TextField(blank=True, null=True)

     class Meta:
         managed = True
         db_table = 'stg_value_datatype'
         verbose_name = 'Data Type'
         verbose_name_plural = 'Data Types'
         ordering = ('name', )

     def __str__(self):
         return self.name #ddisplay disagregation options

     def clean(self):
        if StgValueDatatype.objects.filter(
            name=self.name).count() and not self.valuetype_id:
            raise ValidationError({'name':_(
                'Sorry! This type of data already exists')})

     def save(self, *args, **kwargs):
        super(StgValueDatatype, self).save(*args, **kwargs)


class StgPeriodType(CommonInfo):
    period_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=50, blank=False, null=False,
        default='Not Applicable',verbose_name ='Period Name')
    shortname = models.CharField(max_length=50, blank=True, null=True,
        verbose_name = 'Short Name')
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_time_period'
        verbose_name = 'Periodicity'
        verbose_name_plural = 'Period Types'
        ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay disagregation options

    def clean(self):
        if StgPeriodType.objects.filter(
            name=self.name).count() and not self.period_id:
            raise ValidationError({'name':_(
                'Sorry! Period type with the same name exists')})

    def save(self, *args, **kwargs):
        super(StgPeriodType, self).save(*args, **kwargs)


class StgMeasuremethod(CommonInfo):
    measuremethod_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=230, blank=False, null=False,
        verbose_name = 'Unit of Measure')
    shortname = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(max_length=50, unique=True, blank=True, null=False)
    measure_value = models.DecimalField(max_digits=50, decimal_places=0,
        blank=True, null=True, verbose_name = 'Measure Type')
    description = models.TextField(max_length=200, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_measuremethod'
        verbose_name = 'Indicator Type'
        verbose_name_plural = 'Indicator Types'
        ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay measurement methods

    def clean(self):
        if StgMeasuremethod.objects.filter(
            name=self.name).count() and not self.measuremethod_id:
            raise ValidationError({'name':_(
                'Sorry! Measure type with the same name exists')})

    def save(self, *args, **kwargs):
        super(StgMeasuremethod, self).save(*args, **kwargs)


# In DHIS2, this is the smallest item of a category (Male, Female, 0-4Y, 5+)
class StgDisagregationOptions(CommonInfo):
    categoryoption_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=230, blank=False,
        null=False,)
    shortname = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.BooleanField(default=False)
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_disagregation_options'
        verbose_name = 'Disaggregation'
        verbose_name_plural = 'Disaggregation Options'
        ordering = ('name', )

    def __str__(self):
         return self.name #ddisplay disagregation options

    def clean(self):
        if StgDisagregationOptions.objects.filter(
            name=self.name).count() and not self.categoryoption_id:
            raise ValidationError({'name':_(
                'Sorry! Disaggregation option with same name exists')})

    def save(self, *args, **kwargs):
        super(StgDisagregationOptions, self).save(*args, **kwargs)

# This is a compilation of similar options for disaggregation (sex=Male,Female)
class StgDisagregationCategory(CommonInfo):
    category_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=230, blank=False, null=False,)
    shortname = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    dimension_type = models.CharField(max_length=15, blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    datadimension = models.CharField(max_length=6)
    public_access = models.BooleanField(default=False)
    # this field establishes a many-to-many relationship with the domain table
    category_options = models.ManyToManyField(StgDisagregationOptions,
        db_table='link_category_disaggregate_options',
        blank=True,verbose_name = 'Disaggregation Options')
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_disagregation_category'
        verbose_name = 'Category'
        verbose_name_plural = 'Disaggregation Categories'
        ordering = ('name', )

    def __str__(self):
         return self.name

    def clean(self):
        if StgDisagregationCategory.objects.filter(
            name=self.name).count() and not self.category_id:
            raise ValidationError({'name':_(
                'Sorry! Disaggregation category with same name exists')})

    def save(self, *args, **kwargs):
        super(StgDisagregationCategory, self).save(*args, **kwargs)



# This is logical combination of categories used on datasets eg Age goups and Sex)
class StgCategoryCombination(CommonInfo):
    categorycombo_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=230, blank=False, null=False,)
    shortname = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.BooleanField(default=False)

    # this field establishes a many-to-many relationship with the domain table
    categories = models.ManyToManyField(StgDisagregationCategory,
        db_table='link_categorycombo_categories',blank=True,
        verbose_name = 'Category Combinations')
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_category_combination'
        verbose_name = 'Category Combinations'
        verbose_name_plural = 'Category Combinations'
        ordering = ('name', )

    def __str__(self):
        return self.name #ddisplay measurement methods

    def clean(self):
        if StgCategoryCombination.objects.filter(
            name=self.name).count() and not self.categorycombo_id:
            raise ValidationError({'name':_(
                'Sorry! Category combination with same name exists')})

    def save(self, *args, **kwargs):
        super(StgCategoryCombination, self).save(*args, **kwargs)

#This is option combinations according to string value such as (0-4Y Male, 0-4Y Female)
class StgDisagoptionCombination(CommonInfo):
    disag_optionscombo_id = models.AutoField(primary_key=True)
    uuid = models.CharField(unique=True,max_length=36, blank=False, null=False,
        default=uuid.uuid4,editable=False, verbose_name = 'Universal ID')
    name = models.CharField(max_length=230, blank=False,
        null=False)
    shortname = models.CharField(max_length=150, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    source_system = models.CharField(max_length=100, blank=True, null=True)
    public_access = models.BooleanField(default=False)
    # this field establishes a many-to-many relationship similar to category combinations
    category_options = models.ManyToManyField(StgDisagregationOptions,
        db_table='link_disagoptioncombo_disagoptions',
        blank=True,verbose_name = 'Disaggregation Combinations')
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_disagoption_combination'
        verbose_name = 'Disaggregation Combination'
        verbose_name_plural = 'Disaggregation Combinations'
        ordering = ('name', )

    def __str__(self):
         return self.name #ddisplay disagregation options

    def clean(self):
        if StgDisagoptionCombination.objects.filter(
            name=self.name).count() and not self.disag_optionscombo_id:
            raise ValidationError({'name':_(
                'Sorry! Disaggregation combinations with same name exists')})

    def save(self, *args, **kwargs):
        super(StgDisagoptionCombination, self).save(*args, **kwargs)
