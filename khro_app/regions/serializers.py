from rest_framework.serializers import (
    ModelSerializer, HyperlinkedModelSerializer, HyperlinkedRelatedField)

from khro_app.regions.models import (
    StgLocationLevel, StgEconomicZones, StgLocation)

class StgLocationLevelSerializer(ModelSerializer):
    class Meta:
        model = StgLocationLevel
        fields = ['locationlevel_id', 'type', 'name', 'code', 'description']


class StgEconomicZonesSerializer(ModelSerializer):
    class Meta:
        model = StgEconomicZones
        fields = [
            'economiczone_id', 'name', 'code', 'shortname', 'description']


class StgLocationSerializer(HyperlinkedModelSerializer):
    zone = HyperlinkedRelatedField(
        view_name='api:rg:stg_economic_zones-detail',
        read_only=True
    )
    locationlevel = HyperlinkedRelatedField(
        view_name='api:rg:stg_location_level-detail',
        read_only=True
    )

    class Meta:
        model = StgLocation
        fields = [
            'location_id', 'name', 'shortname', 'code', 'description',
            'zone', 'locationlevel', 'cordinates', 'start_date', 'end_date',
            'source_system', 'public_access', 'sort_order']
