from rest_framework.serializers import (ModelSerializer,
    ReadOnlyField, Serializer)

from khro_app.commodities.models import (StgHealthCommodity, FactHealthCommodities)

class StgProductsSerializer(ModelSerializer):
    class Meta:
        model = StgHealthCommodity
        fields = [
            'product_id', 'uuid', 'name', 'code','units_of_measure',
            'source_system','public_access','sort_order']


class FactProductOrderSerializer(ModelSerializer):
    class Meta:
        model = FactHealthCommodities
        fields = [
            'fact_id','location', 'product','unit_price','num_of_orders',
            'order_quantity', 'issued_quantity','order_amount', 'issue_date',
            'comment','public_access']
