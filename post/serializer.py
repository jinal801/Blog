from rest_framework import serializers

from post.constants import POST_CREATED_MSG, LIKES_COUNT_MSG
from post.models import Like, Post


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for the likes."""

    class Meta:
        model = Like
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the posts."""
    owner = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'description', 'content', 'owner', 'count')

    @staticmethod
    def get_owner(obj):
        return POST_CREATED_MSG.format(
            obj.owner.username if obj.owner else obj.owner)

    @staticmethod
    def get_count(obj):
        return LIKES_COUNT_MSG.format(Like.objects.filter(post=obj).count())