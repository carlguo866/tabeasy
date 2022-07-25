from django.contrib import admin
from django.db import models
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.forms import TextInput, Textarea, Select

from tourney.forms import RoundForm
from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round
from tourney.models.team import Team


class BallotAdmin(admin.ModelAdmin, DynamicArrayMixin):
    model = Ballot

admin.site.register(Ballot, BallotAdmin)


class RoundInline(admin.StackedInline):
    model = Round
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


class BallotInlineAdmin(admin.TabularInline):
    model = Ballot
    fields = ['judge']
    extra = 0
    show_change_link = True

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    inlines = [BallotInlineAdmin]

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    search_fields = ['user.username']
    # fieldsets = (
    #     (None, {'fields': ('ballots', 'pairing1s', 'pairing2s')}),
    # )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    search_fields = ['team_name']


