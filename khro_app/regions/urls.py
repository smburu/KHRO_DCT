from rest_framework.routers import SimpleRouter
from khro_app.regions import views

router = SimpleRouter()
router.register(
    r'stg_location_level', views.StgLocationLevelViewSet, "stg_location_level")
router.register(
    r'stg_economic_zones', views.StgEconomicZonesViewSet, "stg_economic_zones"),
router.register(
    r'stg_location', views.StgLocationViewSet, "stg_location")
urlpatterns = router.urls
