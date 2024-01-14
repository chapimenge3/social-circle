from django.urls import path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r"", views.FriendsView, basename="friends")

urlpatterns = [
    path(
        "friend-request/<int:pk>/",
        views.FriendRequestDetailsView.as_view(),
        name="friend-request-details",
    ),
    path("friend-request/", views.FriendRequestView.as_view(), name="friend-request"),
    path(
        "friend-request/received/",
        views.FriendRequestReceivedView.as_view(),
        name="friend-request-recieved",
    ),
    path(
        "friend-request/accept/<int:pk>/",
        views.AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "friend-request/reject/<int:pk>/",
        views.RejectFriendRequestView.as_view(),
        name="reject-friend-request",
    ),
]

urlpatterns += router.urls
