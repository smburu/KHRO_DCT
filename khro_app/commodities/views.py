from django.shortcuts import render
from rest_framework import viewsets

from khro_app.commodities.models import (StgHealthCommodity, FactHealthCommodities)
from khro_app.commodities.serializers import (
    StgProductsSerializer, FactProductOrderSerializer)


class StgProductsViewSet(viewsets.ModelViewSet):
    queryset = StgHealthCommodity.objects.all()
    serializer_class = StgProductsSerializer


class ProductsorderViewSet(viewsets.ModelViewSet):
    queryset = FactHealthCommodities.objects.all()
    serializer_class = FactProductOrderSerializer
