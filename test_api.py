from django.test import TestCase
from rest_framework.test import APIClient
from base.models import User, SosDevice

class DeviceAssignmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser")
        self.device = SosDevice.objects.create()

    def test_assign_device(self):
        response = self.client.post(f'/devices/{self.device.device_id}/assign/', {
            'user_id': self.user.user_id
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.assigned_device, self.device)
        self.device.refresh_from_db()
        self.assertTrue(self.device.is_assigned)

    def test_send_location_only_if_assigned(self):
        # Not assigned yet
        response = self.client.post(f'/devices/{self.device.device_id}/location/', {
            'latitude': 1.1, 'longitude': 2.2, 'ping_time': '2025-05-27T10:00:00Z'
        }, format='json')
        self.assertEqual(response.status_code, 400)

        # Now assign and retry
        self.user.assigned_device = self.device
        self.user.save()
        self.device.is_assigned = True
        self.device.save()

        response = self.client.post(f'/devices/{self.device.device_id}/location/', {
            'latitude': 1.1, 'longitude': 2.2, 'ping_time': '2025-05-27T10:00:00Z'
        }, format='json')
        self.assertEqual(response.status_code, 200)