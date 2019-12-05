from rest_framework.routers import SimpleRouter
from khro_app.commodities import views

router = SimpleRouter()
router.register(
    r'stg_commodities', views.StgProductsViewSet, "stg_commodities")
router.register(
    r'fact_product_orders', views.ProductsorderViewSet, "fact_commodities_orders")
urlpatterns = router.urls
