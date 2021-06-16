from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('subscribe/', views.user_subscribe, name='subscribe'),
    path('setings/', views.user_settings, name='settings'),
    path('avatar/', views.user_avatar, name='avatar'),
]
