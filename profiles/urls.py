from profiles.views import ProfileViewSet, ProfileDetailView

try:
    from django.urls import path, include
    from rest_framework.routers import DefaultRouter
except ImportError:
    raise ImportError(
        "django and django rest framework needs to be added to INSTALLED_APPS."
    )


router = DefaultRouter()
router.register(r"", ProfileViewSet, basename="profile")

urlpatterns = [
    path("detail/", ProfileDetailView.as_view(), name="profile-detail"),
]
