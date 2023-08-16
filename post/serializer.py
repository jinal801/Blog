from rest_framework import serializers

from post.constants import POST_CREATED_MSG, LIKES_COUNT_MSG, LIKED_MSG
from post.models import Like, Post


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for the likes."""
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'post', 'user')

    @staticmethod
    def get_user(obj):
        """return username of the post liked by any user."""
        return LIKED_MSG.format(
            obj.user.username if obj.user else obj.user)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the posts."""
    owner = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('title', 'description', 'content', 'owner', 'count')

    @staticmethod
    def get_owner(obj):
        """return username of the post owner."""
        return POST_CREATED_MSG.format(
            obj.owner.username if obj.owner else obj.owner)

    @staticmethod
    def get_count(obj):
        """Return total likes for the post."""
        return LIKES_COUNT_MSG.format(Like.objects.filter(post=obj).count())