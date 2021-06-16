from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('explore/', views.ExploreView.as_view(), name='explore'),
    path('post/', views.post_create, name='post_create'),
    path('post/<uuid:uuid>/', views.post_view, name='post'),
    path('post/delete/', views.post_delete, name='post_delete'),
    path('post/like/', views.post_like, name='post_like'),
    path('<slug:slug>/', views.user_profile, name='profile'),
]
