from django.forms.models import modelformset_factory, inlineformset_factory
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, TemplateView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.reverse import reverse_lazy
from unicodedata import category
from articles.forms import ArticleCreateForm, ArticleDisplayForm, EditArticleForm
from articles.models import Article, ArticleSection
from articles.serializers import ArticleSerializer
from common.forms import ArticleSectionItemForm
from common.models import Section


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
            print("Formset errors:", formset.errors)
            return super().form_invalid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/details-article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = self.object.articlesection_set.all()
        return context

class EditArticleView(UpdateView):
    model = Article
    form_class = EditArticleForm
    template_name = 'articles/edit-article.html'

    def get_success_url(self):
        return reverse_lazy('details-article', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = self.object.articlesection_set.all()


        return context

class ListArticlesByCategory(TemplateView):
    template_name = 'articles/list-articles.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.kwargs['category']
        featured_articles = Article.objects.filter(category=category)[:3]
        context['category'] = category
        context['featured_articles'] = featured_articles
        return context

# REST Article list
class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        category = self.kwargs['category']
        return Article.objects.filter(category=category)


