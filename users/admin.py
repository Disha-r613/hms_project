from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_doctor', 'is_patient', 'is_staff')
    list_filter = ('is_doctor', 'is_patient', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('Role', {'fields': ('is_doctor', 'is_patient')}),
    )


admin.site.register(User, CustomUserAdmin)

