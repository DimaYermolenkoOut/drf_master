from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from authentication.models import User
from django.urls import reverse

class TestSetUp(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = User.objects.create_user(username='testuser', password='testpassword')
        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        self.token = self.client.post(self.login_url, self.credentials, format='json').data['token']