from .models import Comment, Reply
from .serialziers import CommentSerializer, ReplySerializer
from api.permissions import UserReplyPermission

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.response import Response


class CommentUserViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    """
    A Custom ViewSet that provides `create`, `list`, and `destory` actions.
    """
    permission_classes = (UserReplyPermission, )
    filter_backends = (DjangoFilterBackend,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    filterset_fields = ['user', 'content', 'pub_date']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
