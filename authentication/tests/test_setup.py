from rest_framework.test import APITestCase
from django.urls import reverse
from authentication.views import RegisterView
from authentication.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# class TestSetup(APITestCase):
#
#     def setUp(self):
        # self.data = {
        #     "email": "dy5780356@gmail",
        #     "username": "dy5780356",
        #     "password": "12345"
        # }
        # self.url = reverse('register')
        # self.response = self.client.post(self.url, self.data, format='json')