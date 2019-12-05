from django.db import models
from khro_app.common_info.models import CommonInfo
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def make_choices(values):
    return [(v, v) for v in values]

# This model defines the levels applicable to continental, regional and country political boundaries
class StgLocationLevel(CommonInfo):
    LEVEL = ('level 1','Level 2','Level 3', 'Level 4', 'Level 5','Level 6','Level 7',)

    locationlevel_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    type = models.CharField(max_length=50, choices=make_choices(LEVEL), default=LEVEL[0],
        verbose_name = 'Location Level')  # Field name made lowercase.
    name = models.CharField(max_length=230, blank=False, null=False,verbose_name = 'Level Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=50, blank=True, null=False)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_location_level'
        verbose_name = 'Level'
        verbose_name_plural = 'Organization Levels'
        ordering = ('code', )

    def __str__(self):
        return self.name #display only the level name

class StgEconomicZones(CommonInfo):
    economiczone_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(max_length=36,blank=False, null=False,verbose_name = 'Universal ID')  # Field name made lowercase.
    name = models.CharField(max_length=230,blank=False, null=False,verbose_name = 'Economic Block')  # Field name made lowercase.
    code = models.CharField(max_length=50, unique=True, blank=True, null=False)  # Field name made lowercase.
    shortname = models.CharField(unique=True,max_length=50, blank=True, null=True,
        verbose_name = 'Short Name')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'stg_economic_zones'
        verbose_name = 'Economic Block'
        verbose_name_plural = 'Manage Economic Blocks'
        ordering = ('code', )

    def __str__(self):
        return self.name #display the data source name


class StgLocation(CommonInfo):
    location_id = models.AutoField(primary_key=True)  # Field name made lowercase.
    uuid = models.CharField(max_length=36,blank=False, null=False,
        verbose_name = 'Universal Key')  # Field name made lowercase.
    name = models.CharField(max_length=230,blank=False, null=False,
        verbose_name = 'Location Name')  # Field name made lowercase.
    shortname = models.CharField(max_length=50, blank=True, null=True,
        verbose_name = 'Short Name')  # Field name made lowercase.
    code = models.CharField(unique=True, max_length=15, blank=True,
        null=False, verbose_name = 'Location Code')  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)  # Field name made lowercase.
    parent = models.ForeignKey('self', models.PROTECT,blank=True, null=True,
        verbose_name = 'Parent Location',
        help_text="You are not allowed to edit this field")  # Field name made lowercase.
    locationlevel = models.ForeignKey('StgLocationLevel', models.PROTECT,
        verbose_name = 'Location Level',
        help_text="You are not allowed to make changes to this Field ")  # Field name made lowercase.
    zone = models.ForeignKey(StgEconomicZones, models.PROTECT, blank=False,
        null=False, verbose_name = 'Economic Block',default=6)  # Field name made lowercase.
    latitude = models.DecimalField(max_digits=20,decimal_places=8,blank=True,
        null=True, verbose_name='Latitude')  # Field name made lowercase.
    longitude = models.DecimalField(max_digits=20,decimal_places=8,blank=True,
        null=True,verbose_name= 'Longitude')  # Field name made lowercase.
    cordinates = models.TextField(blank=True, null=True)  # Field name made lowercase.
    start_date = models.DateTimeField(blank=True, null=True, auto_now_add=True,
        verbose_name = 'Date Created')
    end_date= models.DateTimeField(blank=True, null=True, auto_now=True,
        verbose_name = 'Date Modified')
    source_system = models.CharField(unique=False,max_length=100, blank=True,
        null=False, verbose_name = 'Source Name')
    public_access = models.CharField(max_length=6, blank=False, null=False,
        verbose_name = 'Public Access',default='false')
    sort_order = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'stg_location'
        verbose_name = 'Location' # this is important in the display on change details and the add button
        verbose_name_plural = ' Organization Units'
        ordering = ['name',]

    def __str__(self):
        return self.name #display the location name such country

    # This function makes sure the location name is unique but using and not self.location_id
    # Note that [and not self.location_id] allow only chnages to be made..Courtesy of Daniel 05/07/2019
    def clean(self): # Don not allow location to be duplicated but can be edited and chnages saved
        if StgLocation.objects.filter(name=self.name).count() and not self.location_id:
            raise ValidationError({'name':_(
                'Location with the same name already exists')})

    def save(self, *args, **kwargs):
        super(StgLocation, self).save(*args, **kwargs)
