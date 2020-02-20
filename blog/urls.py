from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='blog'),
    path('<int:pk>/', views.post_detail, name='post detail'),
]