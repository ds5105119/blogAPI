from accounts.serializers import UserSerializer
from profiles.models import Profile

try:
    from rest_framework import serializers
except ImportError:
    raise ImportError("django-rest-framework needs to be added to INSTALLED_APPS.")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "user",
            "bio",
            "link",
            "profile_image",
        )
