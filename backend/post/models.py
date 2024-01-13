from typing import Any
from uuid import uuid4 as uuid
from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.exceptions import ValidationError

User = get_user_model()


def upload_to(instance, filename):
    """
    Helper function to generate the path to upload images and videos.
    File will be placed in MEDIA_ROOT/YYYY/MM/DD/<random_string>.<extension>
    """
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")
    return f'{year}/{month}/{day}/{uuid()}.{filename.split(".")[-1]}'


def post_media_type_validation(value):
    """
    Validate if the file is in the allowed media types
    The List can be found in settings.ALLOWED_POST_MEDIA_TYPES
    """
    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            f"The file is too big. Max size is {settings.MAX_UPLOAD_SIZE/1024/1024}MB"
        )

    if value.content_type not in settings.ALLOWED_POST_MEDIA_TYPES:
        raise ValidationError(
            f"File type not supported. Supported types are {settings.ALLOWED_POST_MEDIA_TYPES}"
        )

    return value


class Like(models.Model):
    liker = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.liker} likes {self.post}"

    class Meta:
        unique_together = ("liker", "post")
        ordering = ("-created_at",)


class Comment(models.Model):
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author} commented on {self.post}"

    class Meta:
        ordering = ("-created_at",)


# class PostMedia(models.Model):
#     '''
#     This Model is designed to store media files in s3 bucket
#     '''
#     object_key = models.CharField(max_length=255)
#     bucket = models.CharField(max_length=255, default=settings.AWS_STORAGE_BUCKET_NAME)


class Post(models.Model):
    author = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(
        upload_to=upload_to, blank=True, validators=[post_media_type_validation]
    )
    video = models.FileField(
        upload_to=upload_to, blank=True, validators=[post_media_type_validation]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.author} posted {self.body}"

    def delete(self, *args: Any, **kwargs: Any) :
        self.is_deleted = True
        return super().delete(*args, **kwargs)

    class Meta:
        ordering = ("-created_at",)
