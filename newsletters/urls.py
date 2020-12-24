from rest_framework.routers import DefaultRouter
from .views import NewslettersViewSet,NewletterListUser
from django.urls import path

router = DefaultRouter()
router.register(r'',NewslettersViewSet)
urlpatterns = router.urls

urlpatterns += [
    path('mysuscritions',NewletterListUser.as_view(),name="expenses")
]