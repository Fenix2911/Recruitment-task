from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, SosDevice

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(SosDevice)
class SosDeviceAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'assigned_user', 'latitude', 'longitude', 'ping_time']