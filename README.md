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

### What If:
>If I had more time, I would explore implementing safeguards to prevent location spam in the API.
>For example, if a device started sending location pings every second instead of every few minutes, I would consider adding a few simple backend measures to reduce unnecessary load:
>Rate limiting – I’d use Django REST Framework’s built-in throttling system or implement a custom throttle class to limit how often a device can post location updates (e.g., once every 30 seconds).
>Cooldown logic – On the database or model level, I could store the timestamp of the last update and ignore any new pings that come in too soon.
>Logging and monitoring – Even a basic logging setup could help identify unusual patterns or devices behaving unexpectedly, so we can take action or investigate further.
>These are just starting points, but I believe small changes like these could help make the system more stable and scalable. As a junior developer, I’m always thinking about how features could be improved with time and feedback.
