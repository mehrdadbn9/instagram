import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView

from content.views import index
from user.views import ProfileDetailView, search

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),

    path('auth/', include('user.urls')),
    path('api/auth/', include('user.api.urls')),
    path('content/', include('content.urls')),
    path('activity/', include('activity.urls')),
    path('relation/', include('relation.urls')),

    path('', index, name='myfriend'),
    # path('', index, name='index'),

    path('search/', search, name='search'),

    path('<str:username>/', ProfileDetailView.as_view(), name='profile')
    # path('<username>/', UserProfile, name='profile'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
