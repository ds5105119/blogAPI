from .views import BoardUserViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'p', BoardUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]