from django.contrib import admin

# Register your models here.

from .models import Post, User,AddictionInfo,UserAddiction

admin.site.register(Post)
admin.site.register(User)
admin.site.register(AddictionInfo)
admin.site.register(UserAddiction)