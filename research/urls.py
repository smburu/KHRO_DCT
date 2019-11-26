from rest_framework.routers import SimpleRouter
from research import views

router = SimpleRouter()
router.register(
    r'stg_research_topic', views.StgResearchTopicViewSet, 'stg_research_topic')
router.register(
    r'stg_knowledge_pipeline_type', views.StgKnowledgePipelineTypeViewSet,
    'stg_knowledge_pipeline_type')
router.register(
    r'stg_knowledge_pipeline', views.StgKnowledgePipelineViewSet,
    'stg_knowledge_pipeline')
router.register(
    r'stg_disease_domain', views.StgDiseaseDomainViewSet,
    'stg_disease_domain')
router.register(
    r'stg_research_themes', views.StgResearchThemesViewSet,
    'stg_research_themes')
router.register(
    r'stg_ethics_committee', views.StgEthicsCommitteeViewSet,
    'stg_ethics_committee')
router.register(
    r'stg_research_proposal', views.StgResearchProposalViewSet,
    'stg_research_proposal')
router.register(
    r'stg_research_publication', views.StgResearchPublicationViewSet,
    'stg_research_publication')
urlpatterns = router.urls
