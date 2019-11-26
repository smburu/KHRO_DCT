from django.contrib import admin
from . import models
from .models import (StgHealthCommodity, FactHealthCommodities,)
from import_export.admin import (ImportExportModelAdmin, ExportMixin,
    ImportMixin,ImportExportActionModelAdmin)
from common_info.admin import (OverideImportExport, OverideExport,
    OverideExportAdmin) #added new override for admin action


import data_wizard #this may be the Godsent solution to data import madness that has refused to go

@admin.register(StgHealthCommodity)
class HealthCommoditiesAdmin(admin.ModelAdmin): #add export action to facilitate export od selected fields
    pass

data_wizard.register(FactHealthCommodities) #register fact_data indicator to allow wizard driven import
@admin.register(FactHealthCommodities)
class FactHealthCommoditiesAdmin(admin.ModelAdmin): #add export action to facilitate export od selected fields
    pass
