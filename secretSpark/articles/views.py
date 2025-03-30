from django.shortcuts import render, redirect

from secretSpark.articles.forms import ArticleCreateForm


# def index(request):
#     context = {
#         'a_form': '',
#     }
#     return render(request, 'common/home.html', context=context)


def create_article(request):

    form = ArticleCreateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect('common/home.html')

    context = {
        "form": form,
    }
    return render(request, 'articles/create_article.html' , context)





