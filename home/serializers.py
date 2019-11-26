from rest_framework.serializers import ModelSerializer

from home.models import (
    StgDatasource, StgDisagregationOptions, StgDisagregationCategory,
    StgCategoryCombination, StgDisagoptionCombination)


class StgDatasourceSerializer(ModelSerializer):
    class Meta:
        model = StgDatasource
        fields = [
            'datasource_id', 'uuid', 'name', 'shortname', 'code',
            'source_type', 'description']


class StgDisagregationOptionsSerializer(ModelSerializer):
    class Meta:
        model = StgDisagregationOptions
        fields = ['categoryoption_id', 'uuid', 'name', 'shortname', 'code',
            'description', 'source_system', 'public_access', 'sort_order',]


class StgDisagregationCategorySerializer(ModelSerializer):
    class Meta:
        model = StgDisagregationCategory
        fields = [
            'category_id', 'uuid', 'name', 'shortname', 'code', 'description',
            'dimension_type', 'source_system', 'datadimension', 'public_access',
            'category_options', 'sort_order',]


class StgCategoryCombinationSerializer(ModelSerializer):
    class Meta:
        model = StgCategoryCombination
        fields = [
            'categorycombo_id', 'uuid', 'name', 'shortname', 'code',
            'description', 'source_system', 'public_access', 'categories',
            'sort_order',]


class StgDisagoptionCombinationSerializer(ModelSerializer):
    class Meta:
        model = StgDisagoptionCombination
        fields = [
            'disag_optionscombo_id', 'uuid', 'name', 'shortname', 'code',
            'description', 'source_system', 'public_access', 'category_options',
            'sort_order',]
