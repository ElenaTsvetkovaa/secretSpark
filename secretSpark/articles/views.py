from django.shortcuts import redirect, render
from secretSpark.articles.forms import ArticleCreateForm
from secretSpark.articles.models import Article


def create_article(request):

    form = ArticleCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('common/home.html')

    context = {
        "form": form,
    }
    return render(request, template_name='articles/create-article.html', context=context)


def edit_article(request, pk: int):
    pass


def delete_article(request, pk: int):
    ...

def details_article(request, pk: int):
    article = Article.objects.get(pk=pk)
    context = {
        "article": article
    }

    return render(request, template_name='articles/details-article.html', context=context)

