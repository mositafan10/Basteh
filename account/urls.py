from django.urls import path, include
from django.contrib import admin
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('signup/verification/', views.verification, name="verification"),
    path('profile/', views.ProfileListCreateView.as_view(), name="profile"),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name="profile_detail"),
    path('users/', views.UserList.as_view(), name="users"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="users_detail"),
    path('users/update/', views.update_user, name="update_user"),
    path('social/<int:pk>/', views.social_detail, name="social"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('signup/user/', views.create_user, name="create_user"),
]