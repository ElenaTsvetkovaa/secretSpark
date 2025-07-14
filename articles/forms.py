from django import forms
from articles.models import Article, ArticleSection


class ArticleBaseForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'category', 'banner', )



class ArticleCreateForm(ArticleBaseForm):

    class Meta(ArticleBaseForm.Meta):
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Create New Article..."
            }),
        }


class EditArticleForm(ArticleBaseForm):
    pass

class ArticleDeleteForm(ArticleBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].disabled = True

class ArticleDisplayForm(ArticleBaseForm):
    pass



