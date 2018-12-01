from django.urls import path
from crawler import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('runmodel', views.run_model, name='runmodel'),
    path('topics', views.get_topics, name='topics'),
    path('articles', views.get_articles, name='articles'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
