# Setup Instructions:

## Create project:
```bash
pip install django djangorestframework
django-admin startproject Recruttask
cd Recruttask
python manage.py startapp base
```
## Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
## Create test data:
```bash
python manage.py shell
pythonfrom base.models import User, SosDevice
```
## Create users
```bash
user1 = User.objects.create(name="John Doe")
user2 = User.objects.create(name="Jane Smith")
print(f"Created users: {user1.id}, {user2.id}")
```
## Create devices
```bash
device1 = SosDevice.objects.create(device_id="ABC123")
device2 = SosDevice.objects.create(device_id="XYZ789")
print(f"Created devices: {device1.device_id}, {device2.device_id}")
```
## Start server:
```bash
python manage.py runserver
```

## Test the API
```bash
# Assign device to user
curl -X POST http://localhost:8000/devices/ABC123/assign/ \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1}'

# Update location
curl -X POST http://localhost:8000/devices/ABC123/location/ \
  -H "Content-Type: application/json" \
  -d '{"latitude": 50.123, "longitude": 19.456}'

# Get user location
curl http://localhost:8000/users/1/location/

# Get all locations
curl http://localhost:8000/map/
```
