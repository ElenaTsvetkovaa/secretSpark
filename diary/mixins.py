

class DiaryFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def form_valid(self, form):
        form.instance.mood_id = int(self.request.POST.get("selected_mood"))
        form.instance.date = self.request.POST.get("selected_date")
        return super().form_valid(form)


