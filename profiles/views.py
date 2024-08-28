from accounts.models import User
from profiles.models import Profile
from profiles.serializers import ProfileSerializer

try:
    from rest_framework import viewsets, status
    from rest_framework.decorators import action
    from rest_framework.response import Response
    from rest_framework.pagination import PageNumberPagination
    from django.db.models import Q
except ImportError:
    raise ImportError('django, django-rest-framework, allauth, dj-rest-accounts needs to be added to INSTALLED_APPS.')


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /profiles/{handle}/: handle을 통해 해당 Profile을 반환.
    GET /profiles/: User의 updated_at 순서로 정렬된 20개씩 페이지네이션된 Profile 리스트 반환.
    GET /profiles/search/?q={query}: User의 handle을 검색하여 Profile들을 updated_at 순서로 정렬하고 20개씩 페이지네이션하여 반환
    """
    serializer_class = ProfileSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return Profile.objects.select_related('user').order_by('-user__updated_at')

    def retrieve(self, request, *args, **kwargs):
        handle = kwargs.get('pk')
        try:
            profile = Profile.objects.select_related('user').get(user__handle=handle)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        queryset = self.get_queryset().filter(user__handle__icontains=query)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)