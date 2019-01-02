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
        self.testuser.delete()


class TestUserProfile(TestCase):
    def setUp(self):
        self.testuser = User(username="user", email="test@mail.com")
        self.testuser.save()

    def test_instance(self):
        self.assertIsInstance(self.testprofile, UserProfileData)

    def test_string_representation(self):
        self.assertEqual(str(self.testprofile), self.testprofile.user.username)

    def test_delete_profile(self):
        self.assertIn(self.testprofile, UserProfileData.objects.all())
        self.testprofile.delete_userprofile()
        self.assertNotIn(self.testprofile, UserProfileData.objects.all())

    def test_save_profile(self):
        self.fuser = User(username="fuser", email="fuser@mail.com")
        self.fuser.save()
        self.fprofile = UserProfileData(user=self.fuser)
        self.assertNotIn(self.fprofile, UserProfileData.objects.all())
        self.fprofile.save()
        self.assertIn(self.fprofile, UserProfileData.objects.all())

   
    def test_search_users(self):
        self.assertIn(self.testprofile, UserProfileData.search_users(
            self.testuser.username))