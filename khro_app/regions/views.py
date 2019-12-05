from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from khro_app.regions.models import (
    StgLocationLevel, StgEconomicZones, StgLocation)
from khro_app.regions.serializers import (
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
