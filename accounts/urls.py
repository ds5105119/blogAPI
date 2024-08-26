from django.urls import include, path
from accounts.views import GoogleLogin, GoogleLoginView, UserFollowingViewSet, UserHandelCreateView
from rest_framework_simplejwt.views import TokenVerifyView, TokenRefreshView

try:
    from django.urls import path
except ImportError:
    raise ImportError('django needs to be added to INSTALLED_APPS.')


urlpatterns = [
    path('google/login/callback/', GoogleLoginView.as_view(), name="google_login_callback",),
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('follow/', UserFollowingViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'delete': 'destroy'
    }), name='user_follow'),
    path('handel/', UserHandelCreateView.as_view(), name='handel'),
]