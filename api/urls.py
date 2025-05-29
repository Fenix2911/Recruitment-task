from django.urls import path
from . import views

urlpatterns = [
    path('devices/<str:device_id>/assign/', views.DeviceAssignView.as_view()),
    path('devices/<str:device_id>/location/', views.DeviceLocationView.as_view()),
    path('users/<int:user_id>/location/', views.UserLocationView.as_view()),
    path('map/', views.MapView.as_view()),
]