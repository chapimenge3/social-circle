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
        "friend-request/accept/",
        views.accept_friend_request,
        name="accept-friend-request",
    )
]

urlpatterns += router.urls
