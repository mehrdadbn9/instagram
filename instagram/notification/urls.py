from django.urls import path
from notification.views import ShowNOtifications, DeleteNotification

urlpatterns = [
    path('<noti_id>', ShowNOtifications, name='show-notifications'),
    path('<noti_id>/delete', DeleteNotification, name='delete-notification'),

]
