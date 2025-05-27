from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    assigned_device = models.OneToOneField('SosDevice', on_delete=models.SET_NULL, null=True, blank=True)


class SosDevice(models.Model):
    device_id = models.AutoField(primary_key=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ping_time = models.DateTimeField(null=True, blank=True)
    is_assigned = models.BooleanField(default=False)
