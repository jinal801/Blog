from rest_framework import viewsets, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from post.constants import POST_DELETED_MSG
from post.models import Like, Post
from post.serializer import LikeSerializer, PostSerializer


class LikeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows like to be viewed or edited.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows like to be viewed or edited.
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
            {'message': "you do not have permission to do this action"},
            status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        """update the post only by it's owner."""
        instance = self.get_object()
        if request.user != instance.owner:
            return Response(
                {'message': "you do not have permission to do this action"},
                status=status.HTTP_403_FORBIDDEN)
