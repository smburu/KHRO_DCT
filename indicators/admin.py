from django.contrib import admin
from django.forms import TextInput,Textarea #for customizing textarea row and column size

from data_wizard.sources.models import FileSource,URLSource #customize import soureces

from itertools import groupby #additional import for managing grouped dropdowm
from django import forms
from . import models
from django.core.exceptions import ValidationError # for custome validation
from django.utils.translation import gettext_lazy as _

from .models import (StgLocation, IndicatorProxy,StgIndicator, StgIndicatorDomain,
    FactDataIndicator,Fact_indicator_archive,StgAnalyticsNarrative,StgIndicatorReference,
    StgNarrative_Type,StgIndicatorNarrative)


from .resources import (
    IndicatorResourceExport, IndicatorResourceImport, AchivedIndicatorResourceExport)

from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportMixin,ImportExportActionModelAdmin)
from import_export.formats import base_formats
from home.models import StgDisagoptionCombination #This are additional imports to override default Django forms
from django.forms.models import ModelChoiceField, ModelChoiceIterator
from django.contrib.auth.decorators import permission_required #for approval actions
from common_info.admin import OverideImportExport, OverideExport, OverideExportAdmin #added new override for admin action

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter, RelatedOnlyDropdownFilter) #custom

import data_wizard #this may be the Godsent solution to data import madness that has refused to go
from indicators.serializers import FactDataIndicatorSerializer

#The following 3 functions are used to register global actions performed on the data. See action listbox
def transition_to_pending (modeladmin, request, queryset):
    queryset.update(comment = 'pending')
transition_to_pending.short_description = "Mark selected as Pending"

def transition_to_approved (modeladmin, request, queryset):
    queryset.update (comment = 'approved')
transition_to_approved.short_description = "Mark selected as Approved"

def transition_to_rejected (modeladmin, request, queryset):
    queryset.update (comment = 'rejected')
transition_to_rejected.short_description = "Mark selected as Rejected"

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


@admin.register(StgIndicator)
class IndicatorAdmin(admin.ModelAdmin): #add export action to facilitate export od selected fields
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':150})},
    }

    fieldsets = (
        ('Primary Details', {
                'fields': ('name','shortname','hiscode','afrocode','measuremethod',) #afrocode may be null
            }),
            ('Detailed Definitions', {
                'fields': ('definition','numerator_description', 'denominator_description',),
            }),
            ('Data Source & Reporting', {
                'fields': ('frame_level','data_sources','periodicity','reference','public_access'),
            }),
        )
    list_display=['name','shortname','code','hiscode','afrocode','definition',]
    list_display_links = ('afrocode', 'name',) #display as clickable link
    search_fields = ('name', 'afrocode') #display search field
    list_per_page = 30 #limit records displayed on admin site to 30

    class Meta:
        exclude = ('date_created','date_lastupdated',) #show only related recor


@admin.register(StgIndicatorDomain)
class IndicatorDomainAdmin(admin.ModelAdmin):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':150})},
    }

    fieldsets = (
        ('Domain Attributes', {
                'fields': ('name', 'shortname','parent','level') #afrocode may be null
            }),
            ('Domain Description', {
                'fields': ('description','indicator'),
            }),
        )

    filter_horizontal = ('indicator',) # this should display an inline with multiselect

    list_display=['code','name','parent', 'description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name','shortname','code') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15

    list_filter = (
        ('parent', RelatedOnlyDropdownFilter,),
    )

    class Meta:
        exclude = ('date_created','date_lastupdated',)


@admin.register(StgIndicatorReference)
class IndicatorRefAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':150})},
    }

    fieldsets = (
        ('Reference Attributes', {
                'fields': ('name','shortname',)
            }),
            ('Description', {
                'fields': ('description',),
            }),
        )
    list_display=['code','name','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)

class IndicatorProxyForm(forms.ModelForm):

    # categoryoption = GroupedModelChoiceField(group_by_field='category_options',
    #     #This queryset was modified by Daniel to order the grouped list by  date created
    #     queryset=StgDisagoptionCombination.objects.all().order_by('category__category_id'),
    # )
    class Meta:
        fields = ('indicator','location', 'categoryoption','start_period', 'end_period','period','value_received')
        model = models.FactDataIndicator

    def clean(self):
        cleaned_data = super().clean()

        indicator_field = 'indicator'
        indicator = cleaned_data.get(indicator_field)

        location_field = 'location'
        location = cleaned_data.get(location_field)

        categoryoption_field = 'categoryoption'
        categoryoption = cleaned_data.get(categoryoption_field)

        start_year_field = 'start_period'
        start_period = cleaned_data.get(start_year_field)

        end_year_field = 'end_period'
        end_period = cleaned_data.get(end_year_field)

        if indicator and location and categoryoption and start_period and end_period:
            if FactDataIndicator.objects.filter(indicator=indicator, location=location,
                categoryoption=categoryoption, start_period=start_period,end_period=end_period).exists():

                """ pop(key) method removes the specified key and returns the corresponding value. Returns error If key does not exist"""
                cleaned_data.pop(indicator_field)  # is also done by add_error
                cleaned_data.pop(location_field)
                cleaned_data.pop(categoryoption_field)
                cleaned_data.pop(start_year_field)
                cleaned_data.pop(end_year_field)

                if end_period < start_period:
                    raise ValidationError({'start_period':_(
                        'Sorry! Ending year cannot be lower than the start year. Please make corrections')})
        return cleaned_data


data_wizard.register(
    "Fact Data Indicator Serializer",FactDataIndicatorSerializer) #register fact_data indicator to allow wizard driven import
@admin.register(FactDataIndicator)
class IndicatorFactAdmin(OverideImportExport,ImportExportActionModelAdmin):
    form = IndicatorProxyForm #overrides the default django form

    """
    Davy requested that a user does not see other countries data. This function does exactly that by filtering location based on logged in user
    For this reason only the country of the loggied in user is displayed whereas the superuser has access to all the countries
    Thanks Good for https://docs.djangoproject.com/en/2.2/ref/contrib/admin/ because is gave the exact logic of achiving this non-functional requirement
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #This works like charm!! only superusers and AFRO admin staff are allowed to view all countries and data
        if request.user.is_superuser or request.user.groups.filter(name__icontains='Admins'):
            return qs #provide access to all instances/rows of fact data indicators
        return qs.filter(location=request.user.location)  #provide access to user's country indicator instances

    """
    Davy requested that the form for data input be restricted to the user's country. Thus, this function is for filtering location to display
    country level. The location is used to fielter the dropdownlist based on the request object's USER, If the user has superuser privileges
    or is a member of AFRO-DataAdmins, he/she can enter data for all the AFRO member countries otherwise, can only enter data for his/her country.
    The order_by('locationlevel', 'location_id') clause make sure that the regional offices are first displayed in ascending order
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs): #to implement user filtering her
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

    #This function is used to get the afrocode from related indicator model for use in list_display
    def get_code(obj):
        return obj.indicator.code
    get_code.admin_order_field  = 'indicator__code'  #Lookup to allow column sorting by CODE
    get_code.short_description = 'Indicator Code'  #Renames the column head

    def get_actions(self, request):
        actions = super(IndicatorFactAdmin, self).get_actions(request)
        if not request.user.has_perm('indicators.approve_factdataindicator'):
           actions.pop('transition_to_approved', None)

        if not request.user.has_perm('indicators.reject_factdataindicator'):
            actions.pop('transition_to_rejected', None)

        if not request.user.has_perm('indicators.delete_factdataindicator'):
            actions.pop('delete_selected', None)
        return actions

    def get_export_resource_class(self):
        return IndicatorResourceExport

    def get_import_resource_class(self):
        return IndicatorResourceImport

    readonly_fields = ('indicator', 'location', 'start_period',)
    fieldsets = ( # used to create frameset sections on the data entry form
        ('Indicator Details', {
                'fields': ('indicator','location', 'categoryoption','datasource','measure_type')
            }),
            ('Reporting Period & Values', {
                'fields': ('start_period','end_period','value_received','numerator_value','denominator_value','min_value','max_value','target_value',),
            }),
        )
    # The list display includes a callable get_afrocode that returns indicator code for display on admin pages
    list_display=['location', 'indicator',get_code,'period','categoryoption','value_received','target_value','datasource',] # ,'get_comment_display'
    list_display_links = ('location',get_code, 'indicator',) #display as clickable link
    search_fields = ('indicator__name', 'location__name','period','indicator__afrocode') #display search field
    # search_fields = ('indicator__afrocode','indicator__name', 'location__name', 'datasource','start_period','end_period',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 30
    list_filter = (
        ('location', RelatedOnlyDropdownFilter,),
        ('categoryoption', RelatedOnlyDropdownFilter,),
        ('period',DropdownFilter),
        ('indicator', RelatedOnlyDropdownFilter,),
    )
    readonly_fields=('comment', ) #this field need to be controlled for data entry. should only be active for the approving authority
    actions =[transition_to_pending, transition_to_approved, transition_to_rejected]


# this class define the fact table as a tubular (not columnar) form for ease of entry as requested by Davy Liboko
class FactIndicatorInline(admin.TabularInline):
    form = IndicatorProxyForm #overrides the default django form
    model = models.FactDataIndicator
    extra = 1 # Very useful in controlling the number of empty rows displayed.In this case zero is ok for insertion or changes

    """
    Davy requested that the form input be restricted to the user's country. Thus, this function is for filtering location to
     display country level. The location is used to fielter the dropdownlist based on the request object's USER, If the user is
    superuser, he/she can enter data for all the AFRO member countries otherwise, can only enter data for his/her country.
    """
    def formfield_for_foreignkey(self, db_field, request =None, **kwargs):
        if db_field.name == "location":
            if request.user.is_superuser:
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country']).order_by('locationlevel', 'location_id') #superuser can access all countries at level 2 in the database
            elif request.user.groups.filter(name__icontains='Admins'): #This works like charm!! only AFRO admin staff are allowed to process all countries and data
                kwargs["queryset"] = StgLocation.objects.filter(
                locationlevel__name__in =['Regional','Country']).order_by('locationlevel', 'location_id')
            else:
                kwargs["queryset"] = StgLocation.objects.filter(location_id=request.user.location_id) #permissions for user country filter---works as per Davy's request
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fields = ('indicator','location', 'datasource','measure_type','start_period','end_period','categoryoption','numerator_value',
                'denominator_value', 'value_received','min_value','max_value','target_value',)


@admin.register(IndicatorProxy)
class IndicatorProxy(OverideExport):

    def has_add_permission(self, request, obj=None): #This function removes the add button on the admin interface
        return False

    resource_class = IndicatorResourceExport #added to customize fields displayed on the import window
    inlines = [FactIndicatorInline] #try tabular form
    readonly_fields = ('code','afrocode', 'name',) # Make it read-only for referential integrity constraunts
    fields = ('name','code','afrocode',)
    list_display=['code','name','afrocode',]
    list_display_links=['code','afrocode', 'name']
    search_fields = ('afrocode','name', 'shortname',) #display search field

@admin.register(Fact_indicator_archive)
class IndicatorFactArchiveAdmin(OverideExportAdmin):

    def has_add_permission(self, request): #removes the add button because no data entry is needed
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_afrocode(obj):
        return obj.indicator.afrocode
    get_afrocode.admin_order_field  = 'indicator__afrocode'  #Lookup to allow column sorting by AFROCODE
    get_afrocode.short_description = 'Indicator Code'  #Renames the column head

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        #This works like charm!! only superusers and AFRO admin staff are allowed to view all countries and data
        if request.user.is_superuser or request.user.groups.filter(name__icontains='Admins'):
            return qs #provide access to all instances/rows of fact data indicators
        return qs.filter(location=request.user.location)  #provide access to user's country indicator instances

    resource_class = AchivedIndicatorResourceExport
    list_display=['location', 'indicator',get_afrocode,'period','categoryoption','value_received','target_value',] #'get_comment_display',
    search_fields = ('indicator__name', 'location__name','period','indicator__afrocode') #display search field
    list_per_page = 50 #limit records displayed on admin site to 50
    list_filter = (
        ('location', RelatedOnlyDropdownFilter,),
        ('indicator', RelatedOnlyDropdownFilter,),
    )

@admin.register(models.StgIndicatorGroup)
class IndicatorGoupAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':150})},
    }

    field = ('name','shortname', 'description',) # used to create frameset sections on the data entry form
    list_display=['code','name','shortname', 'description',]
    list_display_links = ('code', 'name',)
    filter_horizontal = ('indicator',) # this should display an inline with multiselect
    exclude = ('code',)

@admin.register(models.StgIndicatorSuperGroup)
class IndicatorSuperGoupAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':150})},
    }

    field = ('name','shortname','description',) # used to create frameset sections on the data entry form
    list_display=['code','name','shortname', 'description',]
    list_display_links=['code','name','shortname',]
    filter_horizontal = ('indicator_groups',) # this should display an inline with multiselect
    exclude = ('code',)
