from django.contrib import admin
from .models import Post, Comment
from mptt.admin import MPTTModelAdmin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'image_tag']


admin.site.register(Comment, MPTTModelAdmin)
