from .models import Comment, Reply
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'user', 'content']


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['comment', 'user', 'content']