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
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        if self.instance and self.instance.section_id:
            self.fields['title'].initial = self.instance.section.title
            self.fields['content'].initial = self.instance.section.content
            self.fields['image'].initial = self.instance.section.image


    def save(self, commit=True):
        section_data = {
            'title': self.cleaned_data['title'],
            'content': self.cleaned_data['content'],
            'image': self.cleaned_data.get('image') or self.instance.section.image,
        }

        if self.instance.section_id:
            section = self.instance.section
            for key, value in section_data.items():
                setattr(section, key, value)
            section.save()
        else:
            section = Section.objects.create(**section_data)

        self.instance.section = section
        return super().save(commit)

class EditArticleSectionForm(ArticleSectionItemForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing an existing instance, make image field not required
        if self.instance and self.instance.pk:
            self.fields['image'].required = False
