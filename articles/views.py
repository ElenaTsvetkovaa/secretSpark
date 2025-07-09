from django.forms.models import modelformset_factory, inlineformset_factory
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView
from rest_framework.reverse import reverse_lazy
from unicodedata import category

from articles.forms import ArticleCreateForm, ArticleDisplayForm
from articles.models import Article, ArticleSection
from common.forms import ArticleSectionItemForm
from common.models import Section


class ListArticlesByCategory(ListView):
    model = Article
    form = ArticleDisplayForm
    template_name = 'articles/list-articles-by-category.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = Article.objects.filter(category=self.kwargs['category'])
        return queryset

    def get_context_data(
        self, *, object_list = ..., **kwargs
    ):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']

        return context


class ListAllArticles(ListView):
    model = Article
    form = ArticleDisplayForm
    template_name = 'articles/articles-list.html'

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'articles/create-article.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        SectionFormSet = inlineformset_factory(
            parent_model=Article,
            model=ArticleSection,
            form=ArticleSectionItemForm,
            extra=3,
            can_delete=True
        )

        if self.request.POST:
            context['formset'] = SectionFormSet(
                self.request.POST,
                self.request.FILES
            )
        else:
            context['formset'] = SectionFormSet()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save() # this is the Article instance

            for section_form in formset:
                title = section_form.cleaned_data.get('title')
                content = section_form.cleaned_data.get('content')
                image = section_form.cleaned_data.get('image')

                section = Section.objects.create(
                    title=title,
                    content=content,
                    image=image
                )

                ArticleSection.objects.create(
                    article=self.object,
                    section=section
                )

            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/details-article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = self.object.articlesection_set.all()
        return context

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

