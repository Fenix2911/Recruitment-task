from rest_framework.response import Response
from base.models import User, SosDevice

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from base.models import SosDevice, User


@api_view(['POST'])
def assign_device(request, id):
    try:
        device = SosDevice.objects.get(pk=id)
        user_id = request.data.get('user_id')
        user = User.objects.get(pk=user_id)

        # Unassign device from other users
        User.objects.filter(assigned_device=device).exclude(pk=user.pk).update(assigned_device=None)

        # Unassign previous device from this user (if any)
        if user.assigned_device and user.assigned_device != device:
            user.assigned_device.is_assigned = False
            user.assigned_device.save()

        # Assign new device
        user.assigned_device = device
        user.save()

        # Mark device as assigned
        device.is_assigned = True
        device.save()

        return Response({'message': 'Device assigned successfully.'})

    except SosDevice.DoesNotExist:
        return Response({'error': 'Device not found.'}, status=404)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

@api_view(['POST'])
def post_location(request, id):
    try:
        device = SosDevice.objects.get(pk=id)

        if not device.is_assigned:
            return Response({'error': 'Device is not assigned.'}, status=400)

        device.latitude = request.data.get('latitude')
        device.longitude = request.data.get('longitude')
        device.ping_time = request.data.get('ping_time')
        device.save()

        return Response({'message': 'Location updated.'})
    except SosDevice.DoesNotExist:
        return Response({'error': 'Device not found.'}, status=404)

@api_view(['GET'])
def user_location(request, id):
    try:
        user = User.objects.get(pk=id)
        device = user.assigned_device

        if not device:
            return Response({'error': 'No device assigned to user.'}, status=404)

        return Response({
            'latitude': device.latitude,
            'longitude': device.longitude,
            'timestamp': device.ping_time
        })

    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

@api_view(['GET'])
def device_map(request):
    devices = SosDevice.objects.filter(is_assigned=True)
    data = [{
        'device_id': d.device_id,
        'latitude': d.latitude,
        'longitude': d.longitude,
        'timestamp': d.ping_time
    } for d in devices]

    return Response(data)
