from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField, Serializer)

from khro_app.elements.models import (StgDataElement, FactDataElement)

class StgDataElementSerializer(ModelSerializer):
    class Meta:
        model = StgDataElement
        fields = ['dataelement_id', 'uuid', 'name', 'shortname', 'code',
            'dhis_uid', 'description', 'domain_type', 'dimension_type',
            'value_type', 'categoryoption', 'aggregation_type', 'source_system',
            'public_access']


class FactDataElementSerializer(ModelSerializer):
    class Meta:
        model = FactDataElement
        fields = [
            'fact_id', 'dataelement', 'location', 'datasource', 'valuetype',
            'value', 'target_value', 'start_year', 'end_year', 'period',
            'comment']
