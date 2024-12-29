from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView, ChangePasswordView,
    ResetPasswordRequestView, ResetPasswordView, LogoutView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset-password-request/', ResetPasswordRequestView.as_view(), name='reset_password_request'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
