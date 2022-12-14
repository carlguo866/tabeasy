from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# from tabeasy_secrets.secret import TOURNAMENT
from rest_framework.exceptions import ValidationError

from submission.models.ballot import Ballot
from submission.models.captains_meeting import CaptainsMeeting
from submission.models.character import Character
from tourney.models import Competitor, Round
from tourney.models.tournament import Tournament

pd_choices = [
    ('P', 'P'),
    ('D', 'D')
]
role_choices = [
    ('att', 'Attorney'),
    ('wit', 'Witness')
]
subsection_type_choices = [
    ('direct', 'Direct'),
    ('cross', 'Cross'),
    ('statement', 'Statement'),
]
class Section(models.Model):
    name = models.CharField(max_length=40)
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, related_name='sections',
                                    related_query_name='section', null=True)
    def __str__(self):
        return f"{self.tournament} {self.name}"

class SubSection(models.Model):
    name = models.CharField(max_length=40)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='subsections',
                                    related_query_name='subsection')
    side = models.CharField(max_length=40, choices=pd_choices)
    role = models.CharField(max_length=40, choices=role_choices)
    type = models.CharField(max_length=40, choices=subsection_type_choices)
    help_text = models.CharField(max_length=40, null=True, blank=True)
    sequence = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class BallotSection(models.Model):
    ballot =  models.ForeignKey(Ballot, on_delete=models.CASCADE, related_name='sections',
                                    related_query_name='section',null=True)
    subsection =  models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='ballot_sections',
                                    related_query_name='ballot_section',null=True)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(max_length=5000, null=True, blank=True)
    #
    # def clean(self):
    #     if self.ballot.submit and self.score == 0:
    #         raise ValidationError("You can't put in a 0 as your score!")

    def __str__(self):
        return self.subsection.__str__()


class CaptainsMeetingSection(models.Model):
    captains_meeting =  models.ForeignKey(CaptainsMeeting, on_delete=models.CASCADE, related_name='sections',
                                    related_query_name='section',null=True)
    subsection =  models.ForeignKey(SubSection, on_delete=models.CASCADE, related_name='captains_meetings',
                                    related_query_name='captains_meeting',null=True)
    competitor = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_name='roles',
                                    related_query_name='role',null=True)
    character = models.ForeignKey(Character, models.SET_NULL, related_name='round_characters',
                                  related_query_name='round_character', null=True, blank=True)

    def __str__(self):
        return self.subsection.__str__() + self.competitor.__str__()

    def clean(self):
        errors = []

        if errors != []:
            raise ValidationError(errors)


