from django.contrib import admin
from .models import Post, User

class UserAdmin(admin.ModelAdmin):
    """user admin class"""
    list_display = ("username", "email")

# Register your models here.
admin.site.register(Post)
admin.site.register(User, UserAdmin)
