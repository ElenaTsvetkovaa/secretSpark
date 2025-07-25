from django.contrib import admin

from diary.models import Diary, Moods


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):

    list_display = ('date', 'profile')
    list_filter = ('date',)
    readonly_fields = ('profile', )
    search_fields = ('profile__user__username', )

    fieldsets = (
        ('Diary Entry', {
            'fields': ('date', 'content', 'mood'),
        }),
    )

@admin.register(Moods)
class MoodsAdmin(admin.ModelAdmin):

    list_display = ('mood',)
    list_filter = ('mood',)
    search_fields = ('mood', )

