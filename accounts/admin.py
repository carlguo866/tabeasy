from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Judge, Team, Tab
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin




# Register your models here.

class UserAdmin(BaseUserAdmin, DynamicArrayMixin):
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password', 'raw_password')}),
        # (('Personal info'), {'fields': ('team_name', 'school','team_roster')}),
        # (('Round info'), {'fields':('sides','ballots','cs','pd')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('raw_password',) #,'sides','ballots','cs','pd'
admin.site.register(User, UserAdmin)

class JudgeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    model = Judge
admin.site.register(Judge, JudgeAdmin)
admin.site.register(Team)
admin.site.register(Tab)
