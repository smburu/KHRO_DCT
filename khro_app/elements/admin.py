import data_wizard #this may be the Godsent solution to data import madness that has refused to go
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from itertools import groupby #additional import for grouped desaggregation options
from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.contrib import admin
from . import models
from . models import (StgLocation, DataElementProxy, FactDataElement,
    StgDataElement,)
from .resources import (
    FactDataResourceExport, FactDataResourceImport, DataElementExport)
from import_export.admin import (
    ImportExportModelAdmin,ExportMixin, ImportExportActionModelAdmin,)
from import_export.formats import base_formats

#This are additional imports to override the default Django forms
from khro_app.home.models import StgCategoryCombination
from django.forms.models import ModelChoiceField, ModelChoiceIterator
from django.contrib.auth.decorators import permission_required #for approval actions

from khro_app.common_info.admin import OverideImportExport, OverideExport

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter, RelatedOnlyDropdownFilter) #custom

#the following 3 functions are used to register global actions performed on the data. See actions listbox
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(comment = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (comment = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (comment = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"

'''---------------------------------------------------------------------------------------------------
These are ModelAdmins that facilitate viewing of raw data elements from other systems like DHIS2
------------------------------------------------------------------------------------------------------'''

class GroupedModelChoiceIterator(ModelChoiceIterator):
    def __iter__(self):
        if self.field.empty_label is not None:
            yield (u"", self.field.empty_label)
        if self.field.cache_choices:
            if self.field.choice_cache is None:
                self.field.choice_cache = [
                    (self.field.group_label(group), [self.choice(ch) for ch in choices])
                        for group,choices in groupby(self.queryset.all(),
                            key=lambda row: getattr(row, self.field.group_by_field))
                ]
            for choice in self.field.choice_cache:
                yield choice
        else:
            for group, choices in groupby(self.queryset.all(),
	        key=lambda row: getattr(row, self.field.group_by_field)):
                    yield (self.field.group_label(group), [self.choice(ch) for ch in choices])


class GroupedModelChoiceField(ModelChoiceField):
    def __init__(self, group_by_field, group_label=None, cache_choices=False, *args, **kwargs):
        """
        group_by_field is the name of a field on the model
        group_label is a function to return a label for each choice group
        """
        super(GroupedModelChoiceField, self).__init__(*args, **kwargs)
        self.group_by_field = group_by_field
        self.cache_choices = cache_choices
        if group_label is None:
            self.group_label = lambda group: group
        else:
            self.group_label = group_label

    def _get_choices(self):
        """
        Exactly as per ModelChoiceField except returns new iterator class
        """
        if hasattr(self, '_choices'):
            return self._choices
        return GroupedModelChoiceIterator(self)
    choices = property(_get_choices, ModelChoiceField._set_choices)


@admin.register(models.StgDataElement)
class DataElementAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Primary Attributes', {
                'fields': ('name','shortname', 'dhis_uid','description')
            }),
            ('Secondary Attributes', {
                'fields': ('domain_type','dimension_type','value_type',
                'aggregation_type','categoryoption'),
            }),
        )

    resource_class = DataElementExport #added to customize fields displayed on the import window
    list_display=['code','name', 'shortname','description', 'domain_type',]
    list_display_links = ('code', 'name',)

    search_fields = ('name', 'code','domain_type',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    list_filter = (
        ('categoryoption',RelatedOnlyDropdownFilter,), #RelatedDropdownFilter
    )
    exclude = ('startdate','enddate', 'date_created','date_lastupdated',)


class DataElementProxyForm(forms.ModelForm):
    # This was changed to take care of the DHIS2 modelling of disagregation
    categoryoption = GroupedModelChoiceField(group_by_field='categoryoption',
        queryset=StgCategoryCombination.objects.all().order_by(
            'categoryoption__categorycombo_id'),
    )

    def clean(self):
        cleaned_data = super().clean()

        dataelement_field = 'dataelement'
        dataelement = cleaned_data.get(dataelement_field)

        location_field = 'location'
        location = cleaned_data.get(location_field)

        categoryoption_field = 'categoryoption'
        categoryoption = cleaned_data.get(categoryoption_field)

        start_year_field = 'start_year'
        start_year = cleaned_data.get(start_year_field)

        end_year_field = 'end_year'
        end_year = cleaned_data.get(end_year_field)

        if dataelement and location and categoryoption and start_year and end_year:
            if FactDataElement.objects.filter(dataelement=dataelement, location=location, categoryoption=categoryoption,
                start_year=start_year,end_year=end_year).exists():

                """ pop(key) method removes the specified key and returns the corresponding value. Returns error If key does not exist"""
                cleaned_data.pop(dataelement_field)  # is also done by add_error
                cleaned_data.pop(location_field)
                cleaned_data.pop(categoryoption_field)
                cleaned_data.pop(start_year_field)
                cleaned_data.pop(end_year_field)

                if end_year < start_year:
                    raise ValidationError({'start_year':_(
                        'Sorry! Ending year cannot be lower than the start year. Please make corrections')})
        return cleaned_data

    class Meta:
        model = models.FactDataElement
        fields = ('dataelement','location','period', 'datasource','start_year','valuetype',
            'end_year','value','target_value','comment',)


data_wizard.register(FactDataElement) #register fact data element serializer to allow wizard driven import
@admin.register(models.FactDataElement)
class DataElementFactAdmin(OverideImportExport,ImportExportActionModelAdmin):
    form = DataElementProxyForm #overrides the default django form
    """
    Davy requested that a user does not see other countries data. This function does exactly that by filtering location based on logged in user
    For this reason only the country of the loggied in user is displayed whereas the superuser has access to all the countries
    Thanks Good for https://docs.djangoproject.com/en/2.2/ref/contrib/admin/ because is gave the exact logic of achiving this non-functional requirement
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.groups.filter(name__icontains='Admins'):
            return qs #provide access to all instances/rows of fact data elements
        return qs.filter(location=request.user.location) #provide access to user's country instances of data elements

    """
    Davy requested that the form for data input be restricted to the user's country. Thus, this function is for filtering location to
     display country level. The location is used to fielter the dropdownlist based on the request object's USER, If the user is
    superuser, he/she can enter data for all the AFRO member countries otherwise, can only enter data for his/her country.
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs): #to implement user filtering her
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country','County'] ).order_by('locationlevel', 'location_id') #superuser can access all countries at level 2 in the database
            elif request.user.groups.filter(name__icontains='Admins'): #This works like charm!! only AFRO admin staff are allowed to process all countries and data
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country','County']).order_by('locationlevel', 'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(location_id=request.user.location_id) #permissions for user country filter---works as per Davy's request
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    #This function is used to get the afrocode from related indicator model for use in list_display
    def get_afrocode(obj):
        return obj.dataelement.code
    get_afrocode.admin_order_field  = 'dataelement__code'  #Lookup to allow column sorting by AFROCODE
    get_afrocode.short_description = 'Data Element Code'  #Renames column head

    #The following function returns available export formats.
    def get_export_formats(self):
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    def get_import_formats(self):
        """
        Returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_actions(self, request):
        actions = super(DataElementFactAdmin, self).get_actions(request)
        if not request.user.has_perm('elements.approve_factdataelement'):
           actions.pop('transition_to_approved', None)

        if not request.user.has_perm('elements.reject_factdataelement'):
            actions.pop('transition_to_rejected', None)

        if not request.user.has_perm('elements.delete_factdataelement'):
            actions.pop('delete_selected', None)
        return actions

    def get_export_resource_class(self):
        return FactDataResourceExport

    def get_import_resource_class(self):
        return FactDataResourceImport

    fieldsets = ( # used to create frameset sections on the data entry form
        ('Data Element Details', {
                'fields': ('dataelement', 'location','datasource','valuetype',)
            }),
            ('Reporting Period & Value', {
                'fields': ('start_year', 'end_year','value','target_value',),
            }),
        )
    #The list display includes a callable get_afrocode that returns data element code for display on admin pages
    list_display=['location','dataelement',get_afrocode,'period','value','datasource','get_comment_display',]
    list_display_links = ('location', get_afrocode,'dataelement',) #For making the code and name clickable
    search_fields = ('dataelement__name', 'location__name','period','dataelement__code') #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    list_filter = (
        ('location', RelatedOnlyDropdownFilter,),

        ('period',DropdownFilter),
        ('dataelement', RelatedOnlyDropdownFilter,),
    )
    readonly_fields=('comment', 'period', ) #this field need to be controlled for data entry. should only be active for the approving authority
    actions = [transition_to_pending, transition_to_approved, transition_to_rejected]

# this class define the fact table as a tubular (not columnar) form for ease of entry as requested by Davy Liboko
class FactElementInline(admin.TabularInline):
    form = DataElementProxyForm #overrides the default django form
    model = models.FactDataElement
    extra = 1 # Very useful in controlling the number of empty rows displayed.In this case zero is Ok for insertion or changes

    """
    This function is for filtering location to display country level. the database field must be parentid
    for the dropdown list    Note the use of locationlevel__name__in as helper for the name lookup while
    (__in)suffix is a special case that works with tuples in Python.
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country','County']).order_by('locationlevel', 'location_id') #superuser can access all countries at level 2 in the database
            elif request.user.groups.filter(name__icontains='Admins'): #This works like charm!! only AFRO admin staff are allowed to process all countries and data
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country','County']).order_by('locationlevel', 'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(location_id=request.user.location_id) #permissions for user country filter---works as per Davy's request
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fields = ('dataelement','location','datasource', 'valuetype','start_year', 'end_year','value','target_value',)


@admin.register(models.DataElementProxy)
class DataElementProxyAdmin(ExportMixin, admin.ModelAdmin):
    def has_add_permission(self, request, obj=None): #This function removes the add button on the admin interface
        return False

    def get_import_formats(self):  #This function limits the export format to only 3 types -CSV, XML and XLSX
        """
        This function returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_import()]

    def get_export_formats(self):
        """
        This function returns available export formats.
        """
        formats = (
              base_formats.CSV,
              base_formats.XLS,
              base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]

    #list_display_links = ('code', 'name',)
    resource_class = FactDataResourceExport #added to customize fields displayed on the import window

    inlines = [FactElementInline] # Use tabular form within the data element modelform

    fields = ('code', 'name')
    list_display=['code','name', 'domain_type','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('domain_type','code','name',) #display search field
    readonly_fields = ('code','name','description',)



@admin.register(models.StgDataElementGroup)
class DataElementGoupAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    field = ('name','shortname', 'description',) # used to create frameset sections on the data entry form
    list_display=['code','name','shortname', 'description',]
    filter_horizontal = ('dataelement',) # this should display an inline with multiselect
    exclude = ('code',)
