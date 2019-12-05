import uuid
from import_export import resources
from import_export.fields import Field
from .models import FactDataElement
from khro_app.elements.models import StgDataElement
from khro_app.regions.models import StgLocation
from khro_app.home.models import StgCategoryCombination,StgDatasource,StgValueDatatype
from import_export.widgets import ForeignKeyWidget, DateWidget


"""
Davy's Skype 26/10/2018 suggestions - limit fields to be imported/exported
This class requires the methods for saving the instance to be overriden
"""
class FactDataResourceImport(resources.ModelResource):

    def before_save_instance(self, instance, using_transactions, dry_run):
        save_instance(instance, using_transactions=True, dry_run=True)

    def get_instance(self, instance_loader, row):
        return False

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        if dry_run:
            pass
        else:
            instance.save()

    element_code = Field(column_name='Data Element Code', attribute='dataelement',
        widget=ForeignKeyWidget(StgDataElement, 'code'))
    dataelement_name = Field(column_name='Element Name',attribute='dataelement',
        widget=ForeignKeyWidget(StgDataElement, 'name'))
    location_code = Field(column_name='Country Code',attribute='location_code',
        widget=ForeignKeyWidget(StgLocation, 'code'))
    location_name = Field(column_name='Country Name',attribute='location',
        widget=ForeignKeyWidget(StgLocation, 'name'))
    categoryoption = Field( column_name='Disaggregation Code',attribute='categoryoption',
        widget=ForeignKeyWidget(StgCategoryCombination, 'code'))
    categoryoption_name = Field(column_name='Disaggregation Type',attribute='categoryoption__name',
        widget=ForeignKeyWidget(StgCategoryCombination, 'name'))
    datasource = Field( column_name='Data Source',attribute='datasource',
        widget=ForeignKeyWidget(StgDatasource, 'code'))
    valuetype = Field( column_name='Data Type',attribute='valuetype',
        widget=ForeignKeyWidget(StgValueDatatype, 'code'))
    # period = Field(column_name='Period',attribute='period',)
    start_period = Field(attribute='start_year', column_name='Start Period')
    end_period = Field( attribute='end_year', column_name='End Period')



    value = Field(attribute='value', column_name='Value')

    class Meta:
        model = FactDataElement
        skip_unchanged = False
        report_skipped = False
        exclude = ('dataelement_name','location_name','categoryoption_name',)
        fields = ('element_code','location_code','categoryoption_code',
            'start_period','start_period', 'value',)


class FactDataResourceExport(resources.ModelResource):
    location_name = Field(attribute='location__name', column_name='Country')
    dataelement = Field(attribute='dataelement__name', column_name='Data Element Name')
    element_code= Field(attribute='dataelement__code', column_name='Data Element Code')
    categoryoption = Field(attribute='categoryoption', column_name='Modality')
    period = Field( attribute='period', column_name='Period')
    value = Field(attribute='value', column_name='Value')
    datasource = Field(attribute='datasource', column_name='Data Source')
    valuetype = Field(attribute='valuetype', column_name='Data Type')
    comment = Field(attribute='comment', column_name='Approval Status')

    class Meta:
        model = FactDataElement
        skip_unchanged = False
        report_skipped = False
        fields = ('element_code','dataelement', 'location_name', 'categoryoption',
            'period','value','datasource','valuetype','comment',)


class DataElementExport(resources.ModelResource):
    code= Field(attribute='code', column_name='Element Code')
    name = Field(attribute='name', column_name='Element Name')
    shortname = Field(attribute='shortname', column_name='Short Name')
    description = Field(attribute='description', column_name='Description')
    measuremethod = Field(attribute='measuremethod', column_name='Measure Factor')
    aggregation_type = Field(attribute='aggregation_type', column_name='Type of Aggregation')

    class Meta:
        model = StgDataElement
        skip_unchanged = False
        report_skipped = False
        fields = ('code','name', 'location_name', 'shortname','description',
            'measuremethod','aggregation_type')
