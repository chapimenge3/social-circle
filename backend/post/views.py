from django.db.models import Q

from rest_framework import viewsets, serializers
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from social_network.models import Friends

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

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, is_deleted=False)


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


class FeedViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_queryset(self):
        friends = Friends.objects.filter(
            Q(user=self.request.user) | Q(friend=self.request.user),
            accepted_at__isnull=False).values_list('friend', flat=True)
        return Post.objects.filter(author__in=friends)
