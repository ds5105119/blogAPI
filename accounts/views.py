import requests
from accounts.models import User, Follow
from accounts.permissions import FollowPermission, HandelPermission
from accounts.serialziers import CustomSocialLoginSerializer, FollowerSerializer, FollowingSerializer, UserSerializer

try:
    from django.conf import settings
    from django.shortcuts import get_object_or_404
    from rest_framework import status, mixins, generics, viewsets
    from rest_framework.exceptions import ValidationError
    from rest_framework.response import Response
    from rest_framework.views import APIView
    from dj_rest_auth.registration.views import SocialLoginView
    from allauth.socialaccount.providers.oauth2.client import OAuth2Client
    from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
    from rest_framework.permissions import AllowAny
except ImportError:
    raise ImportError('django, django-rest-framework, allauth, dj-rest-accounts needs to be added to INSTALLED_APPS.')


class UserFollowingViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    """
    유저의 팔로워와 팔로잉에 대한 ViewSet입니다.
    GET: 팔로워와 팔로잉 리스트, request: { handel: User.handel }
    POST: 팔로우, request: { user: User, handel: User.handel }
    DELETE: 팔로우 또는 팔로워 삭제, request: { "user": User, "handel": User.handel, "delete_option": "following" | "follower" }
    """
    permission_classes = (FollowPermission,)

    def get_serializer_class(self):
        if self.action == 'create':
            return FollowingSerializer
        elif self.action == 'destroy':
            return FollowerSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        handel = request.GET.get('handel')
        user = get_object_or_404(User, handel=handel)

        following = Follow.objects.filter(follower=user)
        followers = Follow.objects.filter(user=user)

        following_serializer = FollowingSerializer(following, many=True)
        followers_serializer = FollowerSerializer(followers, many=True)

        return Response({
            'following': following_serializer.data,
            'followers': followers_serializer.data
        })

    def perform_create(self, serializer):
        user = self.request.user
        handel = self.request.data.get('handel')
        user_to_follow = get_object_or_404(User, handel=handel)

        if user == user_to_follow:
            raise ValidationError("You cannot follow yourself.")

        serializer.save(follower=user, user=user_to_follow)

    def destroy(self, request, *args, **kwargs):
        user = request.user
        handel = request.data.get('handel')
        instance = get_object_or_404(User, handel=handel)
        delete_option = request.data.get('delete')

        if not delete_option or not handel:
            return Response({"detail": "Invalid request. 'delete' and 'handel' are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if delete_option == "follower":
            follow_instance = Follow.objects.filter(user=user, follower=instance).first()
            if follow_instance:
                follow_instance.delete()
                return Response({"detail": "Follower removed successfully."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "This user is not your follower."}, status=status.HTTP_400_BAD_REQUEST)

        elif delete_option == "following":
            follow_instance = Follow.objects.filter(user=instance, follower=user).first()
            if follow_instance:
                follow_instance.delete()
                return Response({"detail": "Successfully unfollowed."}, status=status.HTTP_204_NO_CONTENT)
            return Response({"detail": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Invalid delete option."}, status=status.HTTP_400_BAD_REQUEST)


class UserHandelCreateView(APIView):
    permission_classes = (HandelPermission, )

    def post(self, request):
        handel = request.POST.get('handel', None)
        if not handel:
            return Response({'error': 'handel not provided'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(handel=handel).exists():
            return Response({'error': 'User handel already exists'}, status=status.HTTP_409_CONFLICT)

        return Response({}, status=status.HTTP_200_OK)


def forward_google_login(code):
    url = BASE_URL + 'accounts/google/login/'
    payload = {"code": code}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)
    return response


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.env('GOOGLE_REDIRECT_URI')
    client_class = OAuth2Client
    serializer_class = CustomSocialLoginSerializer


class GoogleLoginView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)

        response = forward_google_login(code)
        if response.status_code != status.HTTP_200_OK:
            return Response({"error": "Failed to process with GoogleLoginView"}, status=response.status_code)

        user = User.objects.filter(pk=response.json()['user']['pk']).first()
        if not user:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        if not user.handel:
            return Response({'error': 'User does not have handel'}, status=status.HTTP_402_PAYMENT_REQUIRED)

        return Response(response.json(), status=status.HTTP_200_OK)
