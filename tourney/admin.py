from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from tourney.models import Ballot


class BallotAdmin(admin.ModelAdmin, DynamicArrayMixin):
    model = Ballot

admin.site.register(Ballot, BallotAdmin)