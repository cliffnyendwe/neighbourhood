
from django.test import TestCase

# Create your tests here.


from django.test import TestCase
from django.contrib.auth.models import User
from .models import Neighborhood , Profile , Business

class TestUser(TestCase):
    def setUp(self):
        self.testuser = User(username="user", email="test@mail.com")

    def test_instance(self):
        self.assertIsInstance(self.testuser, User)

    def test_save_user(self):
        self.assertFalse(self.testuser in User.objects.all())
        self.testuser.save()
        self.assertTrue(self.testuser in User.objects.all())

    def test_save_profile(self):
        self.fuser = User(username="fuser", email="fuser@mail.com")
        self.fuser.save()


      

   