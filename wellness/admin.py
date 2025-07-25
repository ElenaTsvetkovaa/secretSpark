from django.contrib import admin
from .models import CyclePhase, CycleCalendar

@admin.register(CyclePhase)
class CyclePhaseAdmin(admin.ModelAdmin):

    list_display = ('name',)
    list_filter = ('name', )
    search_fields = ('name', 'description')
    ordering = ('name',)
    fieldsets = (
        ('Phase Details', {
            'fields': ('name', 'description')
        }),
    )

@admin.register(CycleCalendar)
class CycleCalendarAdmin(admin.ModelAdmin):

    list_display = ('profile', 'last_period_date', 'cycle_length', 'period_length')
    list_filter = ('cycle_length', 'period_length')
    search_fields = ('profile__user__username', )
    ordering = ('-last_period_date',)
    fieldsets = (
        ('Cycle Information', {
            'fields': ('profile', 'last_period_date', 'cycle_length', 'period_length')
        }),
    )