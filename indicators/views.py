from django.shortcuts import render
from rest_framework import viewsets

from indicators.models import (
    StgIndicatorReference, StgIndicator, StgIndicatorDomain, FactDataIndicator,
    StgIndicatorGroup, StgIndicatorSuperGroup)
from indicators.serializers import (
    StgIndicatorReferenceSerializer, StgIndicatorSerializer,
    StgIndicatorDomainSerializer, FactDataIndicatorSerializer,
    StgIndicatorGroupSerializer, StgIndicatorSuperGroupSerializer)

class StgIndicatorReferenceViewSet(viewsets.ModelViewSet):
    queryset = StgIndicatorReference.objects.all()
    serializer_class = StgIndicatorReferenceSerializer


class StgIndicatorViewSet(viewsets.ModelViewSet):
    queryset = StgIndicator.objects.all()
    serializer_class = StgIndicatorSerializer


class StgIndicatorDomainViewSet(viewsets.ModelViewSet):
    queryset = StgIndicatorDomain.objects.all()
    serializer_class = StgIndicatorDomainSerializer


class FactDataIndicatorViewSet(viewsets.ModelViewSet):
    queryset = FactDataIndicator.objects.all()
    serializer_class = FactDataIndicatorSerializer


class StgIndicatorGroupViewSet(viewsets.ModelViewSet):
    queryset = StgIndicatorGroup.objects.all()
    serializer_class = StgIndicatorGroupSerializer


class StgIndicatorSuperGroupViewSet(viewsets.ModelViewSet):
    queryset = StgIndicatorSuperGroup.objects.all()
    serializer_class = StgIndicatorSuperGroupSerializer
