from uuid import uuid4 as uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


def user_directory_path(instance, filename):
    """
    Returns path to upload image to
    """
    random_id = uuid().hex
    file_extension = filename.split(".")[-1]
    filename = f"{random_id}.{file_extension}"
    return f"images/{filename}"


class User(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)

    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns string representation of User object
        """
        return self.username

    @property
    def get_full_name(self):
        """
        Returns full name of User object
        """
        return f"{self.first_name} {self.last_name}"

    @property
    def get_short_name(self):
        """
        Returns short name of User object
        """
        return self.first_name

    @property
    def get_short_bio(self, length=100):
        """
        Returns short bio of User object with length of 100 characters(default)

        Args:
            length: integer, length of bio to return (default: 100)
        """
        return self.bio[:length] + "..." if len(self.bio) > length else self.bio
