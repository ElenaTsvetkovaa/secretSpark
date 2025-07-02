from django import forms
from django.template.defaultfilters import title

from articles.models import ArticleSection
from common.models import Section


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'


class ArticleSectionItemForm(forms.ModelForm):

    title = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Section heading...",
            "class": "text-sm px-2 py-1 border border-gray-300 rounded w-full outline-none"
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Enter text...",
            "class": "text-sm px-2 py-1 border border-gray-300 rounded w-full h-24 outline-none"
        })
    )
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            "class": "text-sm"
        })
    )

    class Meta(SectionForm.Meta):
        model = ArticleSection
        fields = []

    # def save(self, commit = True):
    #     # Getting the obj to link the fields to the Section
    #     article_section = super().save(commit=False)
    #
    #     section = article_section.section
    #     section.title =  self.cleaned_data['title']
    #     section.content =  self.cleaned_data['content']
    #     section.image =  self.cleaned_data['image']
    #     section.save()
    #
    #     article_section.section = section
    #     if commit:
    #         article_section.save()
    #
    #     return article_section