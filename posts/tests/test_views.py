from django.test import TestCase, Client
from posts.models import Post
from django.contrib.auth.models import User
from django.test.utils import override_settings
from allauth.account import app_settings as account_settings
from django.urls import reverse
import uuid

@override_settings(
    SOCIALACCOUNT_AUTO_SIGNUP=True,
    ACCOUNT_SIGNUP_FORM_CLASS=None,
    ACCOUNT_EMAIL_VERIFICATION=account_settings.EmailVerificationMethod.NONE  # noqa
)
class PostsViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        number_of_users = 5
        number_of_post_for_each_user = 5

        for user_num in range(number_of_users):
            user = User.objects.create(username=f'user_{user_num}',
                                       email=f'user_{user_num}@mail.com',
                                       password='password')
            user.save()
            for post_num in range(number_of_post_for_each_user):
                post = Post(author=user,
                            text=str(post_num))
                post.save()

        user = User.objects.get(pk=1)
        user.profile.is_finnish_registration = True
        user.profile.save()

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        resp = self.client.get(reverse('posts:feed'))

        self.assertRedirects(resp, '/accounts/login/?next=/')

    def test_explore_view(self):
        resp = self.client.get(reverse('posts:explore'))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), User.objects.get(pk=1).username)
        self.assertTemplateUsed(resp, 'posts/feed.html')

        post_count = Post.objects.all().count()
        self.assertEqual(len(resp.context['posts']), post_count)

    def test_profile_view(self):
        resp = self.client.get(reverse('posts:profile', kwargs={'slug': self.user.username}))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(str(resp.context['user']), 'user_0')
        self.assertTemplateUsed(resp, 'posts/profile.html')

        for post in resp.context['posts']:
            self.assertEqual(post.author, self.user)

        user_post_count = Post.objects.filter(author=self.user).count()
        self.assertEqual(len(resp.context['posts']), user_post_count)

    def test_HTTTP404_for_invalid_post(self):
        user_post_count = Post.objects.all().count()
        random_uuid = uuid.uuid4()
        resp = self.client.get(reverse('posts:post', kwargs={'uuid': random_uuid}))
        self.assertEqual(resp.status_code, 404)

    def test_post_get(self):
        post = Post.objects.last()
        resp = self.client.get(reverse('posts:post', kwargs={'uuid': post.id}))

        self.assertEqual(resp.context['post'].id, post.id)

    def test_post_like(self):
        post = Post.objects.last()
        resp = self.client.get(reverse('posts:post_like', kwargs={'uuid': post.id}))

        likes = Post.objects.get(id=post.id).likes.count()

        self.assertEqual(likes, 1)

        resp = self.client.get(reverse('posts:post_like', kwargs={'uuid': post.id}))

        likes = Post.objects.get(id=post.id).likes.count()

        self.assertEqual(likes, 0)
