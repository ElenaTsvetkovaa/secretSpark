from django.contrib import admin
from django.contrib.admin import register

from wellness.models import Moods


@register(Moods)
class MoodsAdmin(admin.ModelAdmin):
    pass


