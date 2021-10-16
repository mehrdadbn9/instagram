from django.urls import path

from user.views import RegisterView, LoginView, ProfileUpdateView, ProfileDetailView, sign_up, password_change_done, \
    password_change, EditProfile, search

from django.contrib.auth import views as authViews

urlpatterns = [
    # path('search/', search, name='search'),

    path('edit/', EditProfile, name='edit-profile'),
    # path('profile/edit', EditProfile, name='edit-profile'),

    path('signup/', sign_up, name='signup'),
    # path('register/', RegisterView.as_view(), name='auth-register'),

    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    # path('login/', LoginView.as_view(), name='auth-login'),

    path('logout/', authViews.LogoutView.as_view(), {'next_page': 'index'}, name='logout'),
    path('changepassword/', password_change, name='change_password'),
    path('changepassword/done', password_change_done, name='change_password_done'),
    path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
    path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #     path('profile/', ProfileUpdateView.as_view(), name='auth-profile'),
]
