from .models import Post
from rest_framework import serializers
from taggit.serializers import TagListSerializerField, TaggitSerializer


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = ['user', 'category', 'status', 'title', 'excerpt', 'content', 'slug', 'tags']

    def create(self, validated_data):
        tags = super(TaggitSerializer, self).create(validated_data.get('tags'))
        return Post.objects.create(tags=tags, **validated_data)

    def update(self, instance, validated_data):
        tags = super(TaggitSerializer, self).update(instance, validated_data.get('tags'))
        return Post.objects.create(tags=tags, **validated_data)