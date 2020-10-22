from django.contrib import admin
from . import models
from .models import (StgHealthCommodity, FactHealthCommodities,)
from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportMixin,ImportExportActionModelAdmin)
from khro_app.common_info.admin import (OverideImportExport, OverideExport,
    OverideExportAdmin) #added new override for admin action
from import_export.formats import base_formats
from django.forms import TextInput,Textarea #for customizing textarea row and column size
from khro_app.common_info.admin import OverideExport

import data_wizard #this may be the Godsent solution to data import madness that has refused to go

@admin.register(StgHealthCommodity)
class HealthCommoditiesAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
        models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':120})},
    }

    fieldsets = (
        ('Health Commodities Description', {
                'fields': ('name', 'code','units_of_measure','sort_order',) #afrocode may be null
            }),
        )
    list_display=['name','code','units_of_measure']
    list_display_links = ('code', 'name',)
    search_fields = ('name','code') #display search field
    list_per_page = 50 #limit records displayed on admin site to 15

data_wizard.register(FactHealthCommodities) #register fact_data indicator to allow wizard driven import
@admin.register(FactHealthCommodities)
class FactHealthCommoditiesAdmin(OverideExport):
    from django.db import models
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'80'})},
    }

    fieldsets = (
        ('Commodity Description', {
                'fields': ('product','unit_price','comment','public_access')
            }),
            ('Order Details', {
                'fields': ('location','num_of_orders','order_quantity',
                    'issued_quantity','order_amount','issue_date'),
            }),
        )
    list_display=['product','unit_price','order_quantity','issued_quantity',
        'order_amount','issue_date']
    list_display_links = ('product',)
    search_fields = ('product','issue_date') #display search field
    list_per_page = 50 #limit records displayed on admin site to 15
