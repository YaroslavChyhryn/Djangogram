from django.test import TestCase
from accounts.forms import ProfileSettingForm
from django.contrib.auth.models import User


class ProfileSettingFormTest(TestCase):
    def test_profile_form_user_name_max_length(self):
        form = ProfileSettingForm({'first_name': 'test*50'})
        self.assertFalse(form.is_valid())
