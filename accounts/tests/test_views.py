from django.test import TestCase
from django.test import override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.account import app_settings as account_settings


@override_settings(
    SOCIALACCOUNT_AUTO_SIGNUP=True,
    ACCOUNT_SIGNUP_FORM_CLASS=None,
    ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE  # noqa
)
class AccountsViewTest(TestCase):

    def setUp(self):
        self.user = User(username='test_user',
                         email='test@mail.com',
                         password='password')
        self.user.save()
        self.client.force_login(self.user)

    def test_subscription(self):
        another_user = User(username='another_user',
                            email='another_user@mail.com',
                            password='password')
        another_user.save()
        resp = self.client.get(reverse('accounts:subscribe', kwargs={'user_id': another_user.id}))

        self.assertEqual(User.objects.get(pk=1).profile.followers.all().count(), 2)
        self.assertIn(another_user.id, self.user.profile.followers.values_list('pk', flat=True))
