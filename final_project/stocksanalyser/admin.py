from django.contrib import admin
from .models import Article, User, Question, Category, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Category)
admin.site.register(Comment)
