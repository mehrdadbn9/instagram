from django.urls import path
from content.views import index, new_post, post_details, tags, like, MyFriendViewSet
from content.views import PostListCreateAPIView, PostListView, MyFriendViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter

# simple_router = SimpleRouter()
# simple_router.register('myfriend', MyFriendViewSet, basename="myfriend")

urlpatterns = [
    path('api/posts/', PostListCreateAPIView.as_view(), name='posts'),
    # path('posts/', PostListView.as_view(), name='posts'),

    path('', index, name='myfriend'),
    path('newpost/', new_post, name='newpost'),
    path('<uuid:post_id>', post_details, name='postdetails'),

    path('<uuid:post_id>/like', like, name='postlike'),
    path('tag/<slug:tag_slug>', tags, name='tags'),


    #worked properly
    path('post-list/', MyFriendViewSet.as_view({'get': 'list'}), name='post-list'),
    path('post-detail/<int:pk>/', MyFriendViewSet.as_view({'get': 'retrieve'}), name='post-detail'),
]
# urlpatterns += simple_router.urls
