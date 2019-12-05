from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from rest_framework import viewsets
from khro_app.home.models import (
    StgDatasource, StgDisagregationOptions, StgDisagregationCategory,
    StgCategoryCombination, StgDisagoptionCombination)
from khro_app.home.serializers import (
    StgDatasourceSerializer, StgDisagregationOptionsSerializer,
    StgDisagregationCategorySerializer, StgCategoryCombinationSerializer,
    StgDisagoptionCombinationSerializer)

context = {}

class StgDatasourceViewSet(viewsets.ModelViewSet):
    queryset = StgDatasource.objects.all()
    serializer_class = StgDatasourceSerializer


class StgDisagregationOptionsViewSet(viewsets.ModelViewSet):
    queryset = StgDisagregationOptions.objects.all()
    serializer_class = StgDisagregationOptionsSerializer


class StgDisagregationCategoryViewSet(viewsets.ModelViewSet):
    queryset = StgDisagregationCategory.objects.all()
    serializer_class = StgDisagregationCategorySerializer


class StgCategoryCombinationViewSet(viewsets.ModelViewSet):
    queryset = StgCategoryCombination.objects.all()
    serializer_class = StgCategoryCombinationSerializer


class StgDisagoptionCombinationViewSet(viewsets.ModelViewSet):
    queryset = StgDisagoptionCombination.objects.all()
    serializer_class = StgDisagoptionCombinationSerializer


def index(request):
    return render(request, 'index.html', context=context)

def login_view(request):
    if not request.POST.get('username') or not request.POST.get('password'):
        return render(request, 'index.html', context=context)

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')
    else:
        return render(
            request, 'index.html', {
                    'error_message': 'Login Failed! Please enter Valid Username and Password.', })
