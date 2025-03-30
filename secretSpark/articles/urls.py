from django.urls import path

from secretSpark.articles.views import create_article

urlpatterns = [
    path('create-article/', create_article, name='create-article'),
]
