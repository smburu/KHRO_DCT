from django.shortcuts import render
from rest_framework import viewsets

from settings.models import (CustomUser, CustomGroup,)
from settings.serializers import (
    CustomUserSerializer, CustomGroupSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CustomGroupViewSet(viewsets.ModelViewSet):
    queryset = CustomGroup.objects.all()
    serializer_class = CustomGroupSerializer
