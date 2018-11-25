from django.contrib import admin
from .models import Link, Topic, Article, ArticleTopic

admin.site.register([Link, Topic, Article, ArticleTopic])
