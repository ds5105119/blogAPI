from follows.views import FollowingViewSet

try:
    from django.urls import path
except ImportError:
    raise ImportError('django needs to be added to INSTALLED_APPS.')


urlpatterns = [
    path('follow/', FollowingViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'delete': 'destroy'
    }), name='user_follow'),
]