from django.contrib import admin

from .models import Post, Tag, PostTag,Comment

admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(PostTag)
admin.site.register(Comment)
