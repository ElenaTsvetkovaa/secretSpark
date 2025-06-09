from django import forms

from wellness.models import Diary, Moods


class DiaryForm(forms.ModelForm):

    class Meta:
        model = Diary
        fields = ("content", )

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "relative outline-none resize-none size-full mx-auto bg-white "
                             "shadow-lg rounded-md py-12 pl-12 pr-8 notebook-paper",
                }
            ),
        }


class MoodsForm(forms.ModelForm):

    class Meta:
        model = Moods
        fields = "__all__"







