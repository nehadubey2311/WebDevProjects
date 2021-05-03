from django.contrib import admin
from .models import Article, User, Question, Comment

# Register your models here.
admin.site.register(Article)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(Comment)
