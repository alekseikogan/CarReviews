from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import BodyViewSet, CarViewSet, CommentDestroyView, MarkViewSet
from .auth_api import (
    LoginView,
    MeView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    RegisterView,
)

router = DefaultRouter()
router.register('marks', MarkViewSet, basename='mark')
router.register('bodies', BodyViewSet, basename='body')
router.register('cars', CarViewSet, basename='car')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth-refresh'),
    path('auth/me/', MeView.as_view(), name='auth-me'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='auth-password-reset'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='auth-password-reset-confirm'),
    path('comments/<int:pk>/', CommentDestroyView.as_view(), name='comment-destroy'),
    path('', include(router.urls)),
]
