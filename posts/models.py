from django.contrib.auth import models
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_extensions.db import fields
from django.utils.safestring import mark_safe
from easy_thumbnails.fields import ThumbnailerImageField
import uuid
from mptt.models import MPTTModel, TreeForeignKey


class Post(models.Model):
    """
    Post model.
    image_tag used for displaying image in admin
    """
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    image = ThumbnailerImageField(upload_to='posts/%Y/%m/%d',
                                  blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created = fields.CreationDateTimeField()
    updated = fields.ModificationDateTimeField()

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return reverse('posts:post', args=[self.uuid])

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="150" height="150" />' % self.image.url)  # Get Image url

    @property
    def total_likes(self):
        return self.likes.count()

    image_tag.short_description = 'Image'


class Comment(MPTTModel):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    content = models.TextField()
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']

    def __str__(self):
        return f'Comment by {self.user.username}'
