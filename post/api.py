from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework import serializers

from post.constants import POST_DELETED_MSG, PERMISSION_DENIED_MSG, ALREADY_LIKED_MSG
from post.models import Like, Post
from post.serializer import LikeSerializer, PostSerializer


class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows like to be viewed or edited.
    get:
        without parameters returns all the likes.
    get:
        Returns the detail of a like instance
        parameters: ["id"]
    post:
       Returns the detail of created like instance
        parameters: ["post"]
    put:
        Update the detail of a like instance
        parameters: ["post"]
    delete:
        Delete a like instance
        parameters: ["id"]
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if qs.filter(user=request.user, post_id=request.data.get("post")):
            raise serializers.ValidationError(ALREADY_LIKED_MSG)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows post to be viewed or edited.
    get:
        without parameters returns all the posts.
    get:
        Returns the detail of a post instance
        parameters: ["id"]
    post:
       Returns the detail of created like instance
        parameters: ["title", "description", "content"]
    put:
        Update the detail of a like instance
        parameters: ["title", "description", "content"]
    delete:
        Delete a like instance
        parameters: ["id"]
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """destroy the post and display the success message."""
        instance = self.get_object()
        if request.user == instance.owner:
            self.perform_destroy(instance)
            return Response({
                "message": POST_DELETED_MSG
            }, status=status.HTTP_200_OK)
        return Response(
            {'message': PERMISSION_DENIED_MSG},
            status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        """update the post only by its owner."""
        instance = self.get_object()
        if request.user != instance.owner:
            return Response(
                {'message': PERMISSION_DENIED_MSG},
                status=status.HTTP_403_FORBIDDEN)
