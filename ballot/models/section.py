from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# from tabeasy_secrets.secret import TOURNAMENT
from ballot.models import Ballot
from tourney.models import CaptainsMeeting, TeamMember, Round
from tourney.models.tournament import Tournament

pd_choices = [
    ('p', 'Plaintiff'),
    ('d', 'Defense')
]
role_choices = [
    ('att', 'Attorney'),
    ('wit', 'Witness')
]
class Section(models.Model):
    name = models.CharField(max_length=40)
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, related_name='sections',
                                    related_query_name='section', null=True)
    is_statement = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class SubSection(models.Model):
    name = models.CharField(max_length=40)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subsections',
                                    related_query_name='subsection')
    side = models.CharField(max_length=40, choices=pd_choices)
    role = models.CharField(max_length=40, choices=role_choices)
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class RoundSubSection(models.Model):
    round = models.ForeignKey(Round,on_delete=models.CASCADE, related_name='subsections',
                                    related_query_name='subsection',null=True)
    subsection = models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='round_subsections',
                                   related_query_name='round_subsection', null=True)

class BallotSection(models.Model):
    ballot =  models.ForeignKey(Ballot, on_delete=models.CASCADE, related_name='sections',
                                    related_query_name='section',null=True)
    subsection =  models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='ballot_sections',
                                    related_query_name='ballot_section',null=True)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(max_length=5000, null=True, blank=True)


class CaptainsMeetingSection(models.Model):
    captains_meeting =  models.ForeignKey(CaptainsMeeting, on_delete=models.CASCADE, related_name='sections',
                                    related_query_name='section',null=True)
    subsection =  models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='captains_meetings',
                                    related_query_name='captains_meeting',null=True)
    competitor = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='roles',
                                    related_query_name='role',null=True)
