from django.urls import path

from activity.views import CommentCreateAPIView

urlpatterns = [
    path('api/comment/', CommentCreateAPIView.as_view(), name='comments'),
]
