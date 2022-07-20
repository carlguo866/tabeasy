from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Team


# Register your models here.
class TeamAdmin(BaseUserAdmin):
    model = Team

    fieldsets = (
        (None, {'fields': ('username', 'password', 'raw_password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('raw_password',)


admin.site.register(Team, TeamAdmin)
