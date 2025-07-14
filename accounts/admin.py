from django.contrib import admin

from accounts.models import Profile, CustomUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(CustomUser)
class CustomUseruAdmin(admin.ModelAdmin):
    pass