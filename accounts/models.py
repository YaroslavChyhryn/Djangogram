from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_extensions.db.fields import AutoSlugField


class UserProfile(models.Model):
    """
    UserProfile extents Django user model and uses for following. This model creates automatic when new user created.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.CharField(max_length=500, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = ThumbnailerImageField(upload_to='user_avatars/%Y/%m/%d/', blank=True)
    followers = models.ManyToManyField(User, symmetrical=False, blank=True)
    slug = AutoSlugField(populate_from='user__username')
    is_finnish_registration = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_absolute_url(self):
        return reverse('posts:profile', args=[self.user.username])

    @receiver(post_save, sender=User, dispatch_uid="create_profile")
    def update_profile(sender, instance, **kwargs):
        if kwargs["created"]:
            profile = UserProfile.objects.create(user=instance)
            profile.followers.add(instance)
            profile.save()
