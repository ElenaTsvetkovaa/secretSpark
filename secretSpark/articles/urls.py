from django.urls import path
from secretSpark.articles.views import create_article




urlpatterns = [
    path('create_artticle/', create_article, name='create-article'),
]







