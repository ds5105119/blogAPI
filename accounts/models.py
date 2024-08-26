from accounts.managers import UserManager

try:
    from django.db import models
    from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
except ImportError:
    raise ImportError('django needs to be added to INSTALLED_APPS.')


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports using email instead of username.
    password, last_login, is_active are defined by AbstractBaseUser
    is_superuser is defined by PermissionMixin
    """
    # User Field
    handel = models.CharField(max_length=30, unique=True, null=True, blank=False)
    username = models.CharField(max_length=30, null=False, blank=False)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)

    # Manager Field
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'handel'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'


class Profile(models.Model):
    """
    Custom Profile model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_image = models.URLField(max_length=500, null=False, blank=False)


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', 'follower'], name="unique_followers")]
        ordering = ["-created_at"]

    def __str__(self):
        return f'{self.follower} follows {self.user}'
