from rest_framework.routers import SimpleRouter
from khro_app.elements import views

router = SimpleRouter()
router.register(
    r'stg_data_element', views.StgDataElementViewSet, "stg_data_element")
router.register(
    r'fact_data_element', views.FactDataElementViewSet, "fact_data_element")
urlpatterns = router.urls
