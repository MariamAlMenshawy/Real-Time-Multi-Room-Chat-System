from rest_framework.test import APITestCase
from globals.test_objects import create_chat, create_user
from chat.models import ChatRoom
from django.contrib.auth.models import User 

# Create your tests here.

class TestCreateChatRoom(APITestCase):
    def setUp(self):
        self.endpoint = '/api/new_room/'
        self.user = create_user()
        self.room = create_chat(members=[self.user])

    def test_create_room_by_admin_user(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_authenticate(user=self.user)      # بيحط المستخدم المسجل مباشرة في الريكويست
        data = {
            'name': 'Test Room',
            'slug': 'test-room',
            'description': 'Room created by admin',
            'is_private': False,
            'members': [self.user.id],
        }
        res = self.client.post(self.endpoint,data,format='json')
        print(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(
            ChatRoom.objects.filter(slug='test-room').exists()
        )
    
    def test_normal_user_cannot_create_room(self):
        self.client.force_authenticate(user=self.user)      # بيحط المستخدم المسجل مباشرة في الريكويست
        data = {
            'name': 'Test Room 2',
            'slug': 'test-room-2',
            'description': 'This is another test room',
            'is_private': False,
            'members': [self.user.id],
        }
        res = self.client.post(self.endpoint,data,format='json')
        self.assertEqual(res.status_code, 403)



class TestRoomDetails(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.room = create_chat()
        self.endpoint = f'/api/rooms/{self.room.slug}/'

    def test_authenticated_user_can_get_room_details(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.endpoint)    # X Cache MISS - fetching from DB
        print(res.data)
        self.assertEqual(res.status_code, 200)

        res = self.client.get(self.endpoint)     # ✓ Cache HIT
        print(res.data)
        self.assertEqual(res.status_code, 200)


class TestRegister(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.endpoint = '/api/register/'

    def test_register_user(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "12345678"
        }
        res = self.client.post(self.endpoint,data,format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_invalid_data(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
        }
        res = self.client.post(self.endpoint,data,format="json")
        self.assertEqual(res.status_code, 400)

class TestProfile(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.endpoint = '/api/profile/'

    def test_profile_authenticated(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.endpoint)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["username"], "test")
          
    def test_profile_unauthenticated(self):
        res = self.client.get(self.endpoint)
        self.assertEqual(res.status_code,401)
