from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SosDevice(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    assigned_user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ping_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Device {self.device_id}"