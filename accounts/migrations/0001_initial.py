# Generated by Django 3.2 on 2021-05-21 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(blank=True, max_length=500)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('avatar', easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to='user_avatars/%Y/%m/%d/')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='user__username')),
                ('is_finnish_registration', models.BooleanField(default=False)),
                ('followers', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
