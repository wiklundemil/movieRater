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
        #print(self.url)

    def test_signup_user(self):
        data = {
            "username": "Tester1",
            "password": "pwdTester1",
            "email": "Tester1@gmail.com"
        }
        response = self.client.post(self.url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        #user = User.objects.get(**response.data)
        user = User.objects.get(username=data['username'])
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', response.data)
        #print('signup test done')


# noinspection PyTypeChecker
class UserTokenTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username = 'Tester1' , password = 'pwdTester1'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        #print(self.login_url)
        #print(self.logout_url)


    def test_token_user(self):
        data = {
            'username' : 'Tester1',
            'password' : 'pwdTester1'
        }

        login_response = self.client.post(self.login_url, data)
        self.assertEquals(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('token', login_response.data)

        token = login_response.data['token']

        #set token in client header for the next request
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

        logout_response = self.client.post(self.logout_url)

        self.assertEquals(logout_response.status_code, status.HTTP_200_OK)
        self.assertIn('Successfully logged out.', logout_response.data['detail'])

        #chcek that the token has been deleted
        with self.assertRaises(Token.DoesNotExist):
            Token.objects.get(key=token)
