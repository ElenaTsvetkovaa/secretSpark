from django import forms
from wellness.models import CycleCalendar


class CalendarCycleForm(forms.ModelForm):

    class Meta:
        model = CycleCalendar
        fields = ["last_period_date", "period_length", "cycle_length"]

        labels = {
            "last_period_date": "When did your last period start?",
            "cycle_length": "How long does your menstrual cycle last?",
            "period_length": "What is the standard length of your period?"
        }

        widgets = {
            "last_period_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "w-full appearance-none border border-pink-300 cursor-pointer rounded-md px-4 py-2 bg-white "
                             "text-gray-700 text-center focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400"
                }
            ),
            "period_length": forms.Select(
                choices=[(i, str(i)) for i in range (1, 11)],
                attrs={
                    "class": "w-full appearance-none border border-pink-300 cursor-pointer rounded-md px-4 py-2 bg-white "
                             "text-gray-700 text-center focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400"
                }
            ),
            "cycle_length": forms.Select(
                choices=[(i, str(i)) for i in range(21, 40)],
                attrs={
                    "class": "w-full appearance-none border border-pink-300 cursor-pointer rounded-md px-4 py-2 px-5 bg-white "
                             "text-gray-700 text-center focus:outline-none focus:ring-2 focus:ring-pink-400 focus:border-pink-400"
                }
            )
        }