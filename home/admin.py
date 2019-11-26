from django.contrib import admin
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from . import models
from django.contrib.auth.models import User #to be considered in customizing the user admin

from . models import (StgDisagregationOptions,StgDisagregationCategory,StgCategoryCombination,
    StgDatasource,StgDisagoptionCombination,)

from .resources import(DisaggregateCategoryExport,
    DisaggregateOptionExport,MeasureTypeExport,DataTypeExport)
from common_info.admin import OverideImportExport, OverideExport,OverideExportAdmin
from import_export.admin import (ImportExportModelAdmin, ImportExportActionModelAdmin,)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter,
    RelatedOnlyDropdownFilter) #custom


@admin.register(models.StgMeasuremethod)
class MeasuredAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    resource_class = MeasureTypeExport
    list_display=['code','name','measure_value','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    list_filter = (
        ('measure_value',DropdownFilter),
    )
    exclude = ('date_created','date_lastupdated','code',)

@admin.register(models.StgValueDatatype)
class DatatypeAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    resource_class = DataTypeExport
    list_display=['code','name','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name','code',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)

#these two admin classes are suitable for data that requires disaggregation
@admin.register(StgDisagregationCategory)
class Disaggregate_CategoryAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    filter_horizontal = ('category_options',) # this should display an inline with multiselect

    resource_class = DisaggregateCategoryExport #for export only
    list_display=['code','name','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name', 'shortname','code',) #display search field
    list_per_page = 15 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated','code',)

@admin.register(StgDisagregationOptions)
class Disaggregation_OptionsAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }
    fieldsets = (
        ('Disaggregation Attributes', {
                'fields': ('name','shortname',)
            }),
            ('Detailed Description', {
                'fields': ('description',),
            }),
        )

    resource_class = DisaggregateOptionExport #for export only
    list_display=['code','name','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)


@admin.register(StgCategoryCombination)
class Disaggregation_CategoryComboAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Disaggregation Attributes', {
                'fields': ('name','shortname',)
            }),
            ('Detailed Description', {
                'fields': ('description','categories',),
            }),
        )

    filter_horizontal = ('categories',) # this should display an inline with multiselect

    resource_class = DisaggregateOptionExport #for export only
    list_display=['code','name','shortname','description']
    list_display_links = ('code', 'name',)
    search_fields = ('name','categories') #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)


@admin.register(StgDisagoptionCombination)
class Disaggregation_OptionsComboAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':100})},
    }

    fieldsets = (
        ('Disaggregation Attributes', {
                'fields': ('name','shortname',)
            }),
            ('Detailed Description', {
                'fields': ('description',),
            }),
        )

    resource_class = DisaggregateOptionExport #for export only
    list_display=['code','name','shortname','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)



@admin.register(StgDatasource)
class DatasourceAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':150})},
    }

    fieldsets = (
        ('Data source Attributes', {
                'fields': ('name','shortname','source_type',)
            }),
            ('Detailed Description', {
                'fields': ('description',),
            }),
        )
    resource_class = DisaggregateOptionExport #for export only
    list_display=['code','name','description',]
    list_display_links = ('code', 'name',)
    search_fields = ('code','name',) #display search field
    list_per_page = 30 #limit records displayed on admin site to 15
    exclude = ('date_created','date_lastupdated',)
