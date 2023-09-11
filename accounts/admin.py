from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from accounts.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin, DynamicArrayMixin):
    model = User
    list_display = ('id', 'username', 'tournament')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'raw_password', 'tournament')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'is_team', 'is_judge', 'is_superuser')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff',
                       'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('raw_password',) #,'sides','ballots','cs','pd'