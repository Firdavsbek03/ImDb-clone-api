from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class RegisterTestCase(APITestCase):
    def test_register_user(self):
        data={
            'username':'testuser',
            'email':'testuser@gmail.com',
            'password':'anypassword',
            'password2':"anypassword",
        }
        url = reverse('register')
        response=self.client.post(url,data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


class LoginLogoutTestCase(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(
            username="testuser",
            password="anypassword"
        )
        self.token=Token.objects.get(user=self.user)

    def test_login_user(self):
        data={
            'username':'testuser',
            'password':'anypassword'
        }
        url = reverse('login')
        response=self.client.post(url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response=self.client.post(reverse('logout'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
