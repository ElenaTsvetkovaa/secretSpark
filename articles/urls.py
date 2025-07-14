
from django.urls import path, include
from articles import views


urlpatterns = [
    path('create-article/', views.ArticleCreateView.as_view(), name='create-article'),
    path('<int:pk>/', include([
        path('edit-article', views.EditArticleView.as_view(), name='edit-article'),
        # path('delete-article', delete_article, name='delete-article'),
        path('details-article', views.ArticleDetailView.as_view(), name='details-article'),
    ])),
    path('<str:category>/', views.ListArticlesByCategory.as_view(), name='article-category'),
    path('api/<str:category>/', views.ArticleListAPIView.as_view(), name='api-article-category'),
]
