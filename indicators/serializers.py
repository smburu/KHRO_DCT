from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, DecimalField)

from indicators.models import (
    StgIndicatorReference, StgIndicator, StgIndicatorDomain, FactDataIndicator,
    StgIndicatorGroup, StgIndicatorSuperGroup)

class StgIndicatorReferenceSerializer(ModelSerializer):
    class Meta:
        model = StgIndicatorReference
        fields = ['reference_id', 'name', 'shortname', 'code', 'description']


class StgIndicatorSerializer(ModelSerializer):
    class Meta:
        model = StgIndicator
        fields = [
            'indicator_id', 'name', 'code', 'shortname', 'code', 'hiscode',
            'afrocode', 'definition', 'frame_level', 'numerator_description',
            'denominator_description', 'data_sources', 'reference',
            'periodicity', 'public_access']


class StgIndicatorDomainSerializer(ModelSerializer):
    class Meta:
        model = StgIndicatorDomain
        fields = [
            'domain_id', 'name', 'shortname', 'code', 'description',
            'level', 'public_access', 'sort_order']

# This clas overrides the decimal field in order to
# round off the decimal places.
class RoundedDecimalField(DecimalField):
    def validate_precision(self, value):
        return value


class FactDataIndicatorSerializer(ModelSerializer):
    location_name = ReadOnlyField(source='location.name')
    numerator_value = RoundedDecimalField(max_digits=20, decimal_places=3)
    denominator_value = RoundedDecimalField(max_digits=20, decimal_places=3)
    value_received = RoundedDecimalField(max_digits=20, decimal_places=3)
    min_value = RoundedDecimalField(max_digits=20, decimal_places=3)
    max_value = RoundedDecimalField(max_digits=20, decimal_places=3)
    target_value = RoundedDecimalField(max_digits=20, decimal_places=3)

    class Meta:
        model = FactDataIndicator
        fields = [
            'fact_id', 'indicator', 'location', 'location_name', 'numerator_value',
            'categoryoption', 'datasource', 'measure_type', 'numerator_value',
            'denominator_value', 'value_received', 'min_value', 'max_value',
            'target_value', 'start_period', 'end_period', 'period', 'status',
            'comment']

        data_wizard = {
            'header_row': 0,
            'start_row': 1,
            'show_in_list': True,
        }

class StgIndicatorGroupSerializer(ModelSerializer):
    class Meta:
        model = StgIndicatorGroup
        fields = [
            'group_id', 'uuid', 'name', 'shortname', 'code', 'description',
            'source_system', 'public_access', 'sort_order', 'indicator',]


class StgIndicatorSuperGroupSerializer(ModelSerializer):
    class Meta:
        model = StgIndicatorSuperGroup
        fields = [
            'groupset_id', 'uuid', 'name', 'shortname', 'code', 'description',
            'source_system', 'public_access', 'sort_order', 'indicator_groups',] #check misplaced field
