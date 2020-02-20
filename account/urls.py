from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_list),
    path('<int:pk>/', views.profile_detail),
]