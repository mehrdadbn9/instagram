from django.urls import path

from user.api.views import ProfileRetrieveAPIView, ProfileRetrieveUpdateAPIView, ProfileListAPIView

urlpatterns = [
    path('profile/<str:username>/', ProfileRetrieveAPIView.as_view()),
    path('profile/', ProfileRetrieveUpdateAPIView.as_view()),
    path('profile-list/', ProfileListAPIView.as_view()),

]
