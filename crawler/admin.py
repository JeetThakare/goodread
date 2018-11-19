from django.contrib import admin
from .models import Link, Topic, Article

admin.site.register([Link, Topic, Article])
