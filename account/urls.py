from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('signup/', views.signup, name="login"),
    path('signup/verification/', views.verification, name="verification"),
    path('profile/', views.ProfileListCreateView.as_view(), name="profile"),
    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name="profile_detail"),
    path('users/', views.UserList.as_view(), name="users"),
    path('users/<int:pk>/', views.UserDetail.as_view(), name="users_detail"),
    path('social/<int:pk>/', views.social_detail, name="social"),
    path('signup/user/', views.create_user, name="create_user"),
    path('rest_auth/', include('rest_auth.urls')),
    path('rest_auth/registration/', include('rest_auth.registration.urls')),
]