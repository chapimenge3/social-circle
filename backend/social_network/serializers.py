from rest_framework import serializers

from .models import FriendRequest, Friends


class FriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    friend = serializers.ReadOnlyField(source="friend.username")

    class Meta:
        model = FriendRequest
        fields = ("id", "user", "friend", "is_accepted", "created_at", "updated_at", "is_deleted")

    def validate(self, attrs):
        # check if the friend request is update and the user is the same
        user = self.context["request"].user
        if self.instance and user != self.instance.user:
            return serializers.ValidationError("You can't edit this friend request")

        friend = attrs["friend"]
        if user == friend:
            raise serializers.ValidationError(
                "You can't send a friend request to yourself"
            )

        # check if the other friend request already exists
        if FriendRequest.objects.filter(user=friend, friend=user).exists():
            raise serializers.ValidationError(
                "This user already sent you a friend request"
            )

        is_accepted = attrs.get("is_accepted", None)
        if is_accepted and user != friend:
            raise serializers.ValidationError(
                "You can't accept a friend request that is not yours"
            )

        return super().validate(attrs)


class FriendsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    friend = serializers.ReadOnlyField(source="friend.username")
    accepted_at = serializers.ReadOnlyField()

    class Meta:
        model = Friends
        fields = ("id", "user", "friend", "accepted_at", "created_at", "updated_at")

    def validate(self, attrs):
        # check if the friend request is update and the user is the same
        user = self.context["request"].user
        if self.instance and user != self.instance.user:
            return serializers.ValidationError("You can't edit this friend request")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
