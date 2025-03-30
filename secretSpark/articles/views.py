from django.shortcuts import render, redirect

from secretSpark.articles.forms import ArticleCreateForm


def create_article(request):

    form = ArticleCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('articles')







