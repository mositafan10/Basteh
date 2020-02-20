from django.urls import path
from .views import packet_detail, packet_list

urlpatterns = [
    path('packet/', packet_list, name='packet_list'),
    path('packet/<int:pk>', packet_detail, name='packet_detail'),
]