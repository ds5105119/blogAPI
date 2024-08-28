try:
    from django.db import models
    from django.conf import settings
except ImportError:
    raise ImportError('django needs to be added to INSTALLED_APPS.')


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    """
    Custom Profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    link = models.TextField(blank=True)
    profile_image = models.URLField(max_length=500, null=False, blank=False)
