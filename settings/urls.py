from rest_framework.routers import SimpleRouter
from settings import views

router = SimpleRouter()
router.register(
    r'custom_user', views.CustomUserViewSet, "custom_user")
router.register(
    r'custom_user_group', views.CustomGroupViewSet, "custom_user_group")
urlpatterns = router.urls
