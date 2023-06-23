from django.conf import settings
from rest_framework import serializers

from .models import Post, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    post = serializers.ReadOnlyField(source="post.id")

    class Meta:
        model = Comment
        fields = ("id", "author", "body", "created_at", "updated_at")

    def validate(self, attrs):
        # check if the comment is update and the author is the same
        author = self.context["request"].user
        if self.instance and author != self.instance.author:
            return serializers.ValidationError("You can't edit this comment")

        return super().validate(attrs)


class LikeSerializer(serializers.ModelSerializer):
    liker = serializers.ReadOnlyField(source="liker.username")
    post = serializers.ReadOnlyField(source="post.id")
    # post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Like
        fields = ("id", "liker", "post", "created_at", "updated_at", "post_id")

    def validate(self, attrs):
        liker = self.context["request"].user
        post_id = self.context["request"].data.get("post_id")
        if not post_id:
            raise serializers.ValidationError("You must provide a post_id")

        if Like.objects.filter(liker=liker, post=post_id).exists():
            raise serializers.ValidationError("You can't like a post more than once")
        return super().validate(attrs)

    def create(self, validated_data):
        post_id = self.context["request"].data["post_id"]
        post = Post.objects.get(id=post_id)
        validated_data["post"] = post
        validated_data["liker"] = self.context["request"].user
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "body",
            "image",
            "video",
            "created_at",
            "updated_at",
            "comments",
            "likes",
            "like_count",
            "comment_count",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        # check the file size
        image = attrs.get("image")
        video = attrs.get("video")
        media = image or video
        print(image)
        if media:
            if attrs.get("image") and attrs.get("video"):
                raise serializers.ValidationError(
                    "You can't upload both an image and a video"
                )
            if media.size > settings.MAX_UPLOAD_SIZE:
                raise serializers.ValidationError(
                    f"The file is too big. Max size is {settings.MAX_UPLOAD_SIZE/1024/1024}MB"
                )
            if media.content_type not in settings.ALLOWED_POST_MEDIA_TYPES:
                raise serializers.ValidationError(
                    f"File type not supported. Supported types are {settings.ALLOWED_POST_MEDIA_TYPES}"
                )

        return super().validate(attrs)

    def get_like_count(self, obj):
        """
        Returns the number of likes for a post
        """
        return obj.likes.count()

    def get_comment_count(self, obj):
        """
        Returns the number of comments for a post
        """
        return obj.comments.count()

    def update(self, instance, validated_data):
        """
        Update the post. This method is in place not to allow users to update image or video. only the body is allowed to be updated.
        """
        image = validated_data.get("image")
        video = validated_data.get("video")
        if image or video:
            raise serializers.ValidationError(
                "You can't update an image or video through this endpoint"
            )
        return super().update(instance, validated_data)

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not hasattr(request, "user"):
            raise serializers.ValidationError("You must be authenticated")
        validated_data["author"] = request.user
        return super().create(validated_data)
