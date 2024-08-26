import uuid
from .managers import PublishedManager

from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager


def get_undefined_category():
    """
    Callback called by on_delete when the category foreign key of the posts is deleted
    :return: Category object named undefined
    """
    return Category.objects.get_or_create(name='undefined')


class Category(models.Model):
    """
    Custom Category model
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Custom Posts model
    """
    POST_STATUS = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('suspended', 'Suspended'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET(get_undefined_category),
        default=1
    )
    status = models.CharField(
        max_length=20,
        choices=POST_STATUS,
        default='published'
    )
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='uuid')
    tags = TaggableManager(blank=True)

    objects = models.Manager()
    public_objects = PublishedManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        default_manager_name = 'objects'
        ordering = ['-created_at', ]

    def __str__(self):
        return self.title
