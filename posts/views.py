from .models import Post
from .serializers import PostSerializer
from .services import get_presigned_url
from .permissions import PostPermissions

from django.db.models import F
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView


class GetPresignedUrlView(APIView):
    """
    POST /posts/presigned/: get AWS S3 Bucket presigned post url
    """

    permission_classes = (IsAuthenticated,)
    throttle_scope = "GetPresignedUrlView"

    def post(self, request):
        try:
            presigned_url = get_presigned_url()
            return Response(presigned_url)
        except Exception as e:
            return Response({"error": str(e)})


class LatestPostsAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer


class RecommendPostsAPIView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (PostPermissions,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Post.objects.filter(pk=instance.pk).update(views_count=F("views_count") + 1)
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
