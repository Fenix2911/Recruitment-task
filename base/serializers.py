from rest_framework import serializers
from .models import User, SosDevice


class DeviceAssignSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class LocationUpdateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    ping_time = serializers.DateTimeField(required=False)


class UserLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    timestamp = serializers.DateTimeField()


class MapLocationSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    device_id = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    timestamp = serializers.DateTimeField(source='ping_time')

    def get_user(self, obj):
        return {
            'id': obj.assigned_user.id,
            'name': obj.assigned_user.name
        }