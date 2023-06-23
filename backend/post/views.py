from rest_framework import viewsets, serializers
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class CommonViewSet(viewsets.ModelViewSet):
    def is_owner(self, user):
        key = "author"
        obj = self.get_object()
        if not hasattr(obj, key):
            key = "liker"
        return getattr(obj, key) == user

    def perform_update(self, serializer):
        """
        Perform update request if the user is the author of the object.
        """
        user = self.request.user
        if not self.is_owner(user):
            raise serializers.ValidationError("You can't edit this object")
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        """
        Perform delete request if the user is the author of the object.
        """
        user = self.request.user
        if not self.is_owner(user):
            raise serializers.ValidationError("You can't delete this object")
        return super().perform_destroy(instance)


class PostViewSet(CommonViewSet):
    """
    API endpoint that allows posts to be viewed or edited.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class CommentViewSet(CommonViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


class LikeView(CreateAPIView, DestroyAPIView):
    http_method_names = ["post", "delete"]
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer

    def get_queryset(self):
        return Like.objects.filter(liker=self.request.user)

    # def get_object(self):
        # return self.get_queryset().get()
