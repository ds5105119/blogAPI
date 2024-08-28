from .models import Post
from .serializers import PostSerializer
from .permissions import PostPermissions

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class LatestPostsAPIView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PostSerializer


class RecommendPostsAPIView(generics.ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = PostSerializer


class BoardUserViewSet(viewsets.ModelViewSet):
    permission_classes = (PostPermissions, )
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
