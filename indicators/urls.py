from rest_framework.routers import SimpleRouter
from indicators import views

router = SimpleRouter()
router.register(
    r'stg_indicator_ref', views.StgIndicatorReferenceViewSet, "stg_indicator_ref")
router.register(
    r'stg_indicator', views.StgIndicatorViewSet, "stg_indicator")
router.register(
    r'stg_indicator_domain', views.StgIndicatorDomainViewSet, "stg_indicator_domain")
router.register(
    r'fact_data_indicator', views.FactDataIndicatorViewSet, "fact_data_indicator")
router.register(
    r'stg_indicator_group', views.StgIndicatorGroupViewSet, "stg_indicator_group")
router.register(
    r'stg_indicator_supergroup', views.StgIndicatorSuperGroupViewSet, "stg_indicator_supergroup")
urlpatterns = router.urls
