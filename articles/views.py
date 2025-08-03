from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import inlineformset_factory
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, DeleteView
from rest_framework import status
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import Http404
from rest_framework.reverse import reverse_lazy
from articles.choices import ArticleCategories
from articles.forms import ArticleCreateForm, EditArticleForm, SectionForm
from articles.models import Article
from articles.serializers import ArticleSerializer
from articles.models import Section


SectionFormSet = inlineformset_factory(
    parent_model=Article,
    model=Section,
    form=SectionForm,
    extra=3,
    can_delete=True
)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleCreateForm
    template_name = 'articles/create-article.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404("Page not found")
        return super().dispatch(request,  *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('article-category', kwargs={'category': self.object.category})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = SectionFormSet(self.request.POST, self.request.FILES)
        else:
            context['formset'] = SectionFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/details-article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sections'] = self.object.sections.all()
        return context

class EditArticleView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = EditArticleForm
    template_name = 'articles/edit-article.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404("Page not found")
        return super().dispatch(request,  *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('details-article', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            formset = SectionFormSet(
                self.request.POST,
                self.request.FILES,
                instance=self.object
            )
        else:
            # Dynamically override factory to set extra=0 during edit
            SectionFormSetNoExtra = inlineformset_factory(
                parent_model=Article,
                model=Section,
                form=SectionForm,
                extra=0,
                can_delete=True
            )
            formset = SectionFormSetNoExtra(instance=self.object)

        context['formset'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)

        return self.form_invalid(form)

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
        if category in [ArticleCategories.STYLE, ArticleCategories.SELF_IMPROVEMENT, ArticleCategories.WORK_AND_MONEY]:
            return Article.objects.filter(category=category)
        raise Http404("Category not found")

class DeleteAPIView(LoginRequiredMixin, DestroyAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        category = instance.category
        self.perform_destroy(instance)
        return Response(
            {
                "message": "Article successfully deleted.",
                "redirect_url": f"/articles/{category}/"
            },
            status=status.HTTP_200_OK
        )


