from django import forms
from articles.models import Article


class ArticleBaseForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Title"}),
            "content": forms.Textarea(attrs={"placeholder": "Enter text..."}),
        }


class ArticleCreateForm(ArticleBaseForm):
    pass

class ArticleEditForm(ArticleBaseForm):
    pass

class ArticleDeleteForm(ArticleBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True





