from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import redirect, resolve_url


class MyAccountAdapter(DefaultAccountAdapter):
    """
    Custom redirect for AllAuth after login and logout
    """
    def get_login_redirect_url(self, request):
        path = "/{username}/"
        return path.format(username=request.user.username)

    def get_logout_redirect_url(self, request):
        return '/'
