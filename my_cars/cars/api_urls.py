from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import BodyViewSet, CarViewSet, MarkViewSet

router = DefaultRouter()
router.register('marks', MarkViewSet, basename='mark')
router.register('bodies', BodyViewSet, basename='body')
router.register('cars', CarViewSet, basename='car')

urlpatterns = [
    path('', include(router.urls)),
]
