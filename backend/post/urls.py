from rest_framework import routers
from django.urls import path

from . import views

router = routers.DefaultRouter()
router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"comments", views.CommentViewSet, basename="comment")

urlpatterns = [
    path("likes/", views.LikeView.as_view(), name="likes"),
    path("likes/<int:pk>", views.LikeView.as_view(), name="likes-delete")
]

urlpatterns += router.urls

