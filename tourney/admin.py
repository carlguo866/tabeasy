from django.contrib import admin
from django.db import models
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
from django.forms import TextInput, Textarea, Select

from tourney.forms import RoundForm
from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round, CaptainsMeeting
from tourney.models.team import Team, TeamMember


class RoundInline(admin.StackedInline):
    model = Round
    # form = RoundForm
    autocomplete_fields = ['p_team', 'd_team', 'presiding_judge', 'scoring_judge']
    show_change_link = True
    # extra = 0

    # def get_queryset(self, request):
    #     qs = super(RoundInline, self).get_queryset(request)
    #     return qs.filter()


@admin.register(Pairing)
class PairingAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', 'round_num','division']
    inlines = [RoundInline]

@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', 'round', 'judge', 'p_pd', 'd_pd','d_total_score','p_total_score', 'submit']
    list_filter = ['round__pairing', 'judge']
    search_fields = ['judge']
    model = Ballot


class BallotInlineAdmin(admin.TabularInline):
    model = Ballot
    fields = ['judge']
    extra = 0
    show_change_link = True

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ['pk','__str__','p_team','d_team','presiding_judge','scoring_judge']
    inlines = [BallotInlineAdmin]
    search_fields = ['__str__']

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', '__str__']
    search_fields = ['user.username']
    # fieldsets = (
    #     (None, {'fields': ('ballots', 'pairing1s', 'pairing2s')}),
    # )

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['team_id','team_name','division','school']
    search_fields = ['team_name']

@admin.register(TeamMember)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', 'name','team']
    search_fields = ['name']

@admin.register(CaptainsMeeting)
class CaptainsMeetingAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'submit']
    list_filter = ['round__pairing']
    search_fields = ['round__pairing','__str__']