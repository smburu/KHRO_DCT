from django.shortcuts import render

from rest_framework import viewsets

from khro_app.research.models import (
    StgResearchTopic, StgKnowledgePipelineType, StgKnowledgePipeline,
    StgDiseaseDomain, StgResearchThemes, StgEthicsCommittee,
    StgResearchProposal, StgResearchPublication)
from khro_app.research.serializers import (
    StgResearchTopicSerializer, StgKnowledgePipelineTypeSerializer,
    StgKnowledgePipelineSerializer, StgDiseaseDomainSerializer,
    StgResearchThemesSerializer, StgEthicsCommitteeSerializer,
    StgResearchProposalSerializer, StgResearchPublicationSerializer)

class StgResearchTopicViewSet(viewsets.ModelViewSet):
    queryset = StgResearchTopic.objects.all()
    serializer_class = StgResearchTopicSerializer


class StgKnowledgePipelineTypeViewSet(viewsets.ModelViewSet):
    queryset = StgKnowledgePipelineType.objects.all()
    serializer_class = StgKnowledgePipelineTypeSerializer


class StgKnowledgePipelineViewSet(viewsets.ModelViewSet):
    queryset = StgKnowledgePipeline.objects.all()
    serializer_class = StgKnowledgePipelineSerializer


class StgDiseaseDomainViewSet(viewsets.ModelViewSet):
    queryset = StgDiseaseDomain.objects.all()
    serializer_class = StgDiseaseDomainSerializer


class StgResearchThemesViewSet(viewsets.ModelViewSet):
    queryset = StgResearchThemes.objects.all()
    serializer_class = StgResearchThemesSerializer


class StgEthicsCommitteeViewSet(viewsets.ModelViewSet):
    queryset = StgEthicsCommittee.objects.all()
    serializer_class = StgEthicsCommitteeSerializer


class StgResearchProposalViewSet(viewsets.ModelViewSet):
    queryset = StgResearchProposal.objects.all()
    serializer_class = StgResearchProposalSerializer


class StgResearchPublicationViewSet(viewsets.ModelViewSet):
    queryset = StgResearchPublication.objects.all()
    serializer_class = StgResearchPublicationSerializer
