from django.contrib import admin
from django.db import models
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.forms import TextInput, Textarea, Select

from tourney.forms import RoundForm
from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Pairing, PairingItem
from tourney.models.team import Team


class BallotAdmin(admin.ModelAdmin, DynamicArrayMixin):
    model = Ballot

admin.site.register(Ballot, BallotAdmin)


class RoundInline(admin.StackedInline):
    model = PairingItem
    form = RoundForm
    autocomplete_fields = ['p_team', 'd_team']
    extra = 0

    def get_queryset(self, request):
        qs = super(RoundInline, self).get_queryset(request)
        return qs.filter()


@admin.register(Pairing)
class PairingAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['round_num']
    inlines = [RoundInline]

@admin.register(PairingItem)
class RoundAdmin(admin.ModelAdmin):
    pass
    # formfield_overrides = {
    #     models.OneToOneField: {'widget': Select(attrs={'size': '5'})},
    #     models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    # }

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    search_fields = ['user.username']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    search_fields = ['team_name']

