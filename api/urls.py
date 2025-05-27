from django.urls import path
from .views import assign_device, post_location, user_location, device_map

urlpatterns = [
    path('devices/<int:id>/assign/', assign_device),
    path('devices/<int:id>/location/', post_location),
    path('users/<int:id>/location/', user_location),
    path('map/', device_map),
]