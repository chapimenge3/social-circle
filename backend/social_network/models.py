from django.db import models

from authentication.models import User


class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_friend')
    is_accepted = models.BooleanField(default=False)

    # server generated fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.friend}'

    class Meta:
        unique_together = ('created_at', 'user', 'friend')


class Friends(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend')
    accepted_at = models.DateTimeField(null=True, blank=True)

    # server generated fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.user} - {self.friend}'

    class Meta:
        unique_together = ('user', 'friend')

