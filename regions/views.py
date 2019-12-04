from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from regions.models import (
    StgLocationLevel, StgEconomicZones, StgLocation)
from regions.serializers import (
    StgLocationLevelSerializer, StgEconomicZonesSerializer,
    StgLocationSerializer)

class StgLocationLevelViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = StgLocationLevel.objects.all()
    serializer_class = StgLocationLevelSerializer


class StgEconomicZonesViewSet(viewsets.ModelViewSet):
    queryset = StgEconomicZones.objects.all()
    serializer_class = StgEconomicZonesSerializer


class StgLocationViewSet(viewsets.ModelViewSet):

    queryset = StgLocation.objects.all()
    serializer_class = StgLocationSerializer
