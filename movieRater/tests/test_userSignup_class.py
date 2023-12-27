from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse

class UserSignupTest(APITestCase):
    #test for creating a user view

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("signup")

    def test_signup_user(self):

        data = {
            "username": "Tester1",
            "password": "pwdTester1",
            "email": "Tester1@gmail.com"
        }
        response = self.client.post(self.url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(**response.data)
        self.assertTrue(user.check_passwrod(data['password']))
        self.assertNotIn('password', response.data)


class UserLoginTest(APITestCase):
    def setup(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username = "Tester1" , password = "pwdTester1"
        )
        self.login_url = reverse("login")

    def test_login_user(self):
        data = {
            "username" : "Tester1",
            "password" : "pwdTester1"
        }
        response = self.client.post(self.login_url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)




