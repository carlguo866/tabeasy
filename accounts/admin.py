from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from accounts.models import User, Tab


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

admin.site.register(Tab)