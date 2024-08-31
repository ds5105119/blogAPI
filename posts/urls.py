from .views import GetPresignedUrlView, PostViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"p", PostViewSet)

urlpatterns = [
    path("presigned/", GetPresignedUrlView.as_view(), name="get_presigned_url"),
    path("hmm/", include(router.urls)),
]
