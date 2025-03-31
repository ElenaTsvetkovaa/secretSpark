from django.urls import path, include

from secretSpark.articles.views import create_article, edit_article, delete_article, details_article

urlpatterns = [
    path('create-article/', create_article, name='create-article'),
    path('<int:pk>', include([
        path('edit-article', edit_article, name='edit-article'),
        path('delete-article', delete_article, name='delete-article'),
        path('details-article', details_article, name='details-article'),
    ]))
]
