from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'avatar', 'favorite_genre', 'reading_goal', 'email_verified')}),
    )
    list_display = ('username', 'email', 'reading_goal', 'email_verified', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)
