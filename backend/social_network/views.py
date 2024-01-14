from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import viewsets, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from .models import FriendRequest, Friends
from .serializers import FriendRequestSerializer, FriendsSerializer


User = get_user_model()


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = FriendRequest.objects.filter(
            user=request.user, is_deleted=False, is_accepted=False
        )
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        # User can't send a friend request to himself
        # User can't send a friend request to a user that already sent him a friend request
        #   (even if he didn't accept it yet or rejected it.)
        # User can't send a friend request to a user that he already sent a friend with.

        friend = request.data.get("friend")
        if friend == request.user.id:
            return Response(
                data={"detail": "You can't send a friend request to yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            friend_obj = User.objects.get(id=friend)
        except User.DoesNotExist:
            return Response(
                data={"detail": "This user doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if FriendRequest.objects.filter(Q(user=friend, friend=request.user) | Q(user=request.user, friend=friend)).exists():
            return Response(
                data={"detail": "This user already sent you a friend request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Friends.objects.filter(user=friend, friend=request.user).exists():
            return Response(
                data={"detail": "You are already friends with this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request = FriendRequest.objects.create(
            user=request.user, friend=friend_obj
        )
        serializer = FriendRequestSerializer(friend_request)

        return Response(serializer.data)

    # TODO: Delete friend request
    # def delete(self, request, pk):
    #     instance = self.get_object(pk)
    #     if instance.user != request.user:
    #         return Response(
    #             data={"detail": "You can't delete this friend request"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     instance.is_deleted = True
    #     instance.save()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequestDetailsView(APIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names = ["get", "delete"]
    lookup_field = "pk"

    def get_queryset(self):
        return FriendRequest.objects.filter(
            user=self.request.user, is_deleted=False, is_accepted=False
        )

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs.get("pk"))
        except FriendRequest.DoesNotExist:
            return None

    def get(self, request, pk):
        friend_request = self.get_object()
        if not friend_request:
            return Response(
                data={"detail": "This friend request doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)

    def delete(self, request, pk):
        friend_request = self.get_object()
        if not friend_request:
            return Response(
                data={"detail": "This friend request doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if friend_request.user != request.user:
            return Response(
                data={"detail": "You can't delete this friend request"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request.is_deleted = True
        friend_request.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequestReceivedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = FriendRequest.objects.filter(
            friend=request.user, is_deleted=False, is_accepted=False
        )
        serializer = FriendRequestSerializer(queryset, many=True)
        return Response(serializer.data)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FriendRequest.objects.filter(
                is_deleted=False, is_accepted=False, friend=self.request.user
            ).get(pk=pk)
        except FriendRequest.DoesNotExist:
            return None

    def post(self, request, pk):
        # User can't accept a friend request that is not his
        # User can't accept a friend request that is already accepted
        # User can't accept a friend request that is already rejected
        # User can't accept a friend request that is deleted
        # User can't accept a friend request that doesn't exist
        # User can't accept a friend request that is his
        # User can't accept a friend request that is already a friend

        try:
            friend_request = self.get_object(pk)
        except FriendRequest.DoesNotExist:
            raise serializers.ValidationError(
                "This friend request doesn't exist")

        if friend_request.is_accepted:
            raise serializers.ValidationError(
                "This friend request is already accepted")

        friend_request.is_accepted = True
        friend_request.save()

        Friends.objects.create(user=friend_request.user,
                               friend=friend_request.friend)

        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendsSerializer
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        return Friends.objects.filter(
            user=self.request.user, is_deleted=False
        )

    def get_object(self):
        try:
            return self.get_queryset().get(pk=self.kwargs.get("pk"))
        except Friends.DoesNotExist:
            return None

    def destroy(self, request, pk):
        friend = self.get_object()
        if not friend:
            return Response(
                data={"detail": "This friend doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if friend.user != request.user:
            return Response(
                data={"detail": "You can't delete this friend"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend.is_deleted = True
        friend.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
