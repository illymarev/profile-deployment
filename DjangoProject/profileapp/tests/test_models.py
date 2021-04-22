from django.test import TestCase
from django.contrib.auth import get_user_model
from profileapp import models


class ModelTests(TestCase):

    def test_create_user_successful(self):
        """Test creating a new user is successful"""
        username = 'testusername'
        password = 'testpass123@'
        user = get_user_model().objects.create(
            username=username,
            password=password
        )

        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
