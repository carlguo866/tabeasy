from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from submission.admin import BallotInlineAdmin
from tourney.models.captains_meeting import Character, CharacterPronouns
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round, CaptainsMeeting
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

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['team_id','team_name','division','school']
    search_fields = ['team_name']

@admin.register(Competitor)
class TeamAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ['pk', 'name','team']
    search_fields = ['name']


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'side']
    # list_filter = ['tournament']
    search_fields = ['__str__']

class CharacterPronounsInlineAdmin(admin.TabularInline):
    model = CharacterPronouns
    fields = ['character','pronouns']
    extra = 0
    show_change_link = True

@admin.register(CaptainsMeeting)
class CaptainsMeetingAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__', 'submit']
    list_filter = ['round__pairing']
    inlines = [CharacterPronounsInlineAdmin]
    search_fields = ['round__pairing','__str__']


