from django.contrib import admin
#from django.contrib.admin import display
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from submission.admin import BallotInlineAdmin
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round
from tourney.models.team import Team
from tourney.models.competitor import Competitor
from tourney.models.tournament import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name']


class RoundInline(admin.StackedInline):
    model = Round
    autocomplete_fields = ['p_team', 'd_team', 'presiding_judge', 'scoring_judge']
    show_change_link = True
    extra = 0

    # def get_queryset(self, request):
    #     qs = super(RoundInline, self).get_queryset(request)
    #     return qs.filter()


@admin.register(Pairing)
class PairingAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', 'round_num','division']
    inlines = [RoundInline]

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ['pk','__str__','p_team','d_team','presiding_judge','scoring_judge']
    inlines = [BallotInlineAdmin]
    search_fields = ['__str__']

@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', '__str__']
    search_fields = ['user.username']

    # @display(ordering='user__tournament', description='Tournament')
    # def get_tournament(self, obj):
    #     return obj.user.tournament

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['team_id','team_name','division','school']
    search_fields = ['team_name']

    # @display(ordering='user__tournament', description='Tournament')
    # def get_tournament(self, obj):
    #     return obj.user.tournament

@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', 'name','team']
    search_fields = ['name']




