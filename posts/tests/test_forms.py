from django.test import TestCase
from posts.forms import PostCreateForm


class PostCreateFormTest(TestCase):
    def test_post_text_max_length(self):
        form = PostCreateForm({'text': 'test'*500})
        self.assertFalse(form.is_valid())
