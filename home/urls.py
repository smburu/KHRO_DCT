from rest_framework.routers import SimpleRouter
from home import views

router = SimpleRouter()
router.register(
    r'stg_data_source', views.StgDatasourceViewSet, "stg_data_source")
router.register(
    r'stg_disagregation_options', views.StgDisagregationOptionsViewSet,
    "stg_disagregation_options")
router.register(
    r'stg_disagregation_category', views.StgDisagregationCategoryViewSet,
    "stg_disagregation_category")
router.register(
    r'stg_category_combination', views.StgCategoryCombinationViewSet,
    "stg_category_combination")
router.register(
    r'stg_disagoption_combination', views.StgDisagoptionCombinationViewSet,
    "stg_disagoption_combination")
urlpatterns = router.urls
