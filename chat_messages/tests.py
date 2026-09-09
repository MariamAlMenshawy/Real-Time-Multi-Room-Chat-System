from rest_framework.test import APITestCase
from globals.test_objects import create_chat_message , create_user ,create_chat

class TestMessageHistory(APITestCase):
    def setUp(self):
        self.member = create_user(username='member')
        self.non_member = create_user(username='nonmember')
        self.room = create_chat(members=[self.member])   # بعتنا الميمبر بس
        self.message = create_chat_message(
            room = self.room,
            sender = self.member
        )
        self.endpoint = f'/api/rooms/{self.room.slug}/messages/'

    def test_message_history(self):
        self.client.force_authenticate(user=self.member)
        res = self.client.get(self.endpoint) # X Cache MISS - fetching from DB
        print(res.data)
        self.assertEqual(res.status_code, 200)  

        res = self.client.get(self.endpoint) # ✓ Cache HIT
        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_non_member_cannot_get_messages(self):
        self.client.force_authenticate(user=self.non_member)
        res = self.client.get(self.endpoint)
        print(res.data)
        print(res.status_code)
        self.assertEqual(res.status_code, 403)