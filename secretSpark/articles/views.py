from django.shortcuts import redirect, render
from secretSpark.articles.forms import ArticleCreateForm


def create_article(request):

    form = ArticleCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('common/home.html')

    context = {
        "form": form,
    }
    return render(request, 'articles/create-article.html', context)





