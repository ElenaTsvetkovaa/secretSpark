
from django.urls import path, include

from articles import views
from articles.views import edit_article, delete_article, details_article

urlpatterns = [
    path('', views.ListAllArticles.as_view(), name='articles-list'),

    path('create-article/', views.ArticleCreateView.as_view(), name='create-article'),
    path('<int:pk>/', include([
        path('edit-article', edit_article, name='edit-article'),
        path('delete-article', delete_article, name='delete-article'),
        path('details-article', views.ArticleDetailView.as_view(), name='details-article'),
    ])),
    path('<category>/', views.ListArticlesByCategory.as_view(), name='article-category'),
]
