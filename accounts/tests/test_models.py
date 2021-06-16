from django.test import TestCase
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.urls import reverse


class TestPost(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User(username='test_user',
                         email='test@mail.com',
                         password='password')
        test_user.save()

    def test_user_get_absolute_url(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.profile.get_absolute_url(), '/profile/test_user/')

    def test_creation_user_profile(self):
        user = User.objects.create(username='test')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
