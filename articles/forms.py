from django import forms
from articles.models import Article, Section


class ArticleBaseForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'category', 'banner')


class ArticleCreateForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Create New Article..."
            }),
        }


class EditArticleForm(ArticleBaseForm):
    class Meta(ArticleBaseForm.Meta):
        widgets = {
            "banner": forms.FileInput(attrs={
                "class": "hidden"
            }),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['title', 'content', 'image']
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Section heading...",
                "class": "text-sm px-2 py-1 border border-gray-300 rounded w-full outline-none"
            }),
            "content": forms.Textarea(attrs={
                "placeholder": "Enter text...",
                "class": "text-sm px-2 py-1 border border-gray-300 rounded w-full min-h-[40vh] resize-y outline-none"
            }),
            "image": forms.FileInput(attrs={
                "class": "text-sm"
            })
        }
