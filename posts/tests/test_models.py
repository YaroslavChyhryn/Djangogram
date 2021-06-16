from django.test import TestCase
from posts.models import Post
from django.contrib.auth.models import User


class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User(username='test_user',
                         email='test@mail.com',
                         password='test_user_password')
        test_user.save()
        test_post = Post(author=test_user)
        test_post.save()

    def test_post_get_absolute_url(self):
        post = Post.objects.last()
        self.assertEqual(post.get_absolute_url(), f'/post/{post.id}/')
