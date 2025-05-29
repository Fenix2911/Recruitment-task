from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from base.models import User, SosDevice
from base.serializers import (
    DeviceAssignSerializer,
    LocationUpdateSerializer,
    UserLocationSerializer,
    MapLocationSerializer
)


class DeviceAssignView(APIView):
    def post(self, request, device_id):
        device = get_object_or_404(SosDevice, device_id=device_id)

        serializer = DeviceAssignSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        user = get_object_or_404(User, id=serializer.validated_data['user_id'])

        # Unassign device from previous user
        if device.assigned_user:
            device.assigned_user = None
            device.save()

        # Unassign any existing device from this user
        old_device = SosDevice.objects.filter(assigned_user=user).first()
        if old_device:
            old_device.assigned_user = None
            old_device.save()

        # Assign device to user
        device.assigned_user = user
        device.save()

        return Response({'message': 'Device assigned successfully'})


class DeviceLocationView(APIView):
    def post(self, request, device_id):
        device = get_object_or_404(SosDevice, device_id=device_id)

        if not device.assigned_user:
            return Response({'error': 'Device not assigned'}, status=400)

        serializer = LocationUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        device.latitude = serializer.validated_data['latitude']
        device.longitude = serializer.validated_data['longitude']
        device.ping_time = serializer.validated_data.get('ping_time') or timezone.now()
        device.save()

        return Response({'message': 'Location updated'})


class UserLocationView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        try:
            device = user.sosdevice
            if not device.latitude or not device.longitude:
                return Response({'error': 'No location data'}, status=404)

            data = {
                'latitude': device.latitude,
                'longitude': device.longitude,
                'timestamp': device.ping_time
            }
            serializer = UserLocationSerializer(data)
            return Response(serializer.data)

        except SosDevice.DoesNotExist:
            return Response({'error': 'No device assigned'}, status=404)


class MapView(APIView):
    def get(self, request):
        devices = SosDevice.objects.filter(
            assigned_user__isnull=False,
            latitude__isnull=False,
            longitude__isnull=False
        ).select_related('assigned_user')

        serializer = MapLocationSerializer(devices, many=True)
        return Response(serializer.data)