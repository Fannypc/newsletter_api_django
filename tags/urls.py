from rest_framework.routers import DefaultRouter
from .views import TagsViewSet


router = DefaultRouter()
router.register(r'', TagsViewSet)
urlpatterns = router.urls
