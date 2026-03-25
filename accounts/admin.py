from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'reading_goal', 'email_verified', 'is_staff')
    
    # Filters in the right sidebar
    list_filter = ('email_verified', 'is_staff', 'is_superuser', 'groups')
    
    # Fields to search
    search_fields = ('username', 'email')
    
    # Fieldsets for the edit form - FIXED: favorite_genre (singular)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'bio', 'avatar')}),
        ('Reading Preferences', {'fields': ('favorite_genre', 'reading_goal')}),  # Changed to favorite_genre
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'reading_goal'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('last_login', 'date_joined')

# Register the model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)