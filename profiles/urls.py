from django.urls import path
from profiles.views import ProfileView

try:
    from django.urls import path
except ImportError:
    raise ImportError('django needs to be added to INSTALLED_APPS.')


urlpatterns = [
    path('', ProfileView.as_view(), name="profile",),
]