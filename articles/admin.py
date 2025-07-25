from django.contrib import admin

from articles.models import Article, Section

class SectionInline(admin.StackedInline):
    MAX_ALLOWED_SECTIONS = 3

    model = Section
    extra = 0
    max_num = MAX_ALLOWED_SECTIONS # to keep the integrity of all articles
    fields = ('title', 'content', 'image')
    can_delete = True

    def has_add_permission(self, request, obj):
        if obj and obj.sections.count() > self.MAX_ALLOWED_SECTIONS:
            return False
        return super().has_add_permission(request, obj)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'banner')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

    fieldsets = (
        ('Article Info', {
            'fields': ('title', 'category', 'banner'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    inlines = [SectionInline]

