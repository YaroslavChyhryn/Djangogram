from django import forms
from accounts.models import UserProfile
from allauth.account.forms import SignupForm
from datetime import datetime

current_year = datetime.today().year
YEARS = list(range(current_year, current_year-100,-1))


class ProfileSettingForm(forms.Form):
    """
    Form for update user profile fields
    """
    first_name = forms.CharField(label='Имя', max_length=50,
                                 widget=forms.TextInput(),
                                 required=False)
    last_name = forms.CharField(label='Фамилия', max_length=50,
                                widget=forms.TextInput(),
                                required=False)
    user_name = forms.CharField(label='Отображаимое имя пользователя', max_length=50,
                                widget=forms.TextInput(),
                                required=True)
    bio = forms.CharField(label='Биография', max_length=500,
                          required=False)
    date_of_birth = forms.DateField(label='Дата рождения', widget=forms.SelectDateWidget(years=YEARS),
                                    required=True)


class AvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']
