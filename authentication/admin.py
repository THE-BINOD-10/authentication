from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'created_at', 'updated_at']
    list_filter = ['is_staff', 'is_admin', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']  # Change ordering to 'email'
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_admin', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_admin'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
