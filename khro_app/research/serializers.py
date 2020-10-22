from rest_framework.serializers import (
    ModelSerializer, ReadOnlyField)

from khro_app.research.models import (
    StgResearchTopic, StgKnowledgePipelineType, StgKnowledgePipeline,
    StgDiseaseDomain, StgResearchThemes, StgEthicsCommittee,
    StgResearchProposal)

class StgResearchTopicSerializer(ModelSerializer):
    class Meta:
        model = StgResearchTopic
        fields = [
            'topic_id', 'uuid', 'name', 'shortname', 'code',
            'description', 'source_system', 'public_access', 'sort_order']


class StgKnowledgePipelineTypeSerializer(ModelSerializer):
    class Meta:
        model = StgKnowledgePipelineType
        fields = [
            'type_id', 'uuid', 'name', 'code', 'description']


class StgKnowledgePipelineSerializer(ModelSerializer):
    class Meta:
        model = StgKnowledgePipeline
        fields = [
            'product_id', 'uuid', 'code', 'title', 'description',
            'type', 'location', 'topic', 'public_access']


class StgDiseaseDomainSerializer(ModelSerializer):
    location_name = ReadOnlyField(source='location.name')

    class Meta:
        model = StgDiseaseDomain
        fields = [
            'domain_id', 'uuid', 'name', 'shortname', 'code', 'description',
            'parent', 'level', 'source_system', 'public_access', 'sort_order',
            'location_name']


class StgResearchThemesSerializer(ModelSerializer):
    location_name = ReadOnlyField(source='location.name')

    class Meta:
        model = StgResearchThemes
        fields = [
            'theme_id', 'uuid', 'name', 'shortname', 'code', 'description',
            'source_system', 'public_access', 'sort_order', 'location_name']


class StgEthicsCommitteeSerializer(ModelSerializer):
    class Meta:
        model = StgEthicsCommittee
        fields = [
            'rec_id', 'uuid', 'name', 'shortname', 'location', 'code',
            'license_number', 'authorization', 'latitude', 'longitude',
            'start_date', 'end_date', 'status_note', 'source_system',
            'public_access', 'sort_order']


class StgResearchProposalSerializer(ModelSerializer):
    class Meta:
        model = StgResearchProposal
        fields = [
            'product', 'erc', 'research_objective', 'principal_researcher',
            'research_team', 'num_of_researchers', 'affiliate_insititutions',
            'funding_source', 'start_date', 'end_date', 'approval_status',
            'sort_order']
