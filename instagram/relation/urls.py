from django.urls import path

from relation.views import FollowView, FollowBackListAPIView

urlpatterns = [
    # path('follow/', FollowView.as_view, name='follow-unfollow')
    path('<str:username>/follow/', FollowView.as_view(), name='follow'),
    path('follow-back/', FollowBackListAPIView.as_view(), name='follower'),
]
