from django.db import models

from submission.models.captains_meeting import CaptainsMeeting
from tourney.models import Tournament

pronoun_choices = [
    ('he', 'he/him'),
    ('she', 'she/her'),
    ('they','they/them'),
    ('ze','ze/hir')
]
side_choices = [
    ('P', 'P'),
    ('D', 'D'),
    ('other','Other'),
]

class Character(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='characters',
                                    related_query_name='character', null=True)
    name = models.CharField(max_length=50, default='')
    side = models.CharField(max_length=5, choices=side_choices, null=True)
    def __str__(self):
        return self.name

class CharacterPronouns(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='characters',
                                  related_query_name='character')
    captains_meeting = models.ForeignKey(CaptainsMeeting, on_delete=models.CASCADE, related_name='captains_meetings',
                                  related_query_name='captains_meeting')
    pronouns = models.CharField(max_length=20, choices=pronoun_choices, null=True)

    def __str__(self):
        if self.pronouns == None:
            return self.character.__str__()
        else:
            for (i, j) in pronoun_choices:
                if i == self.pronouns:
                    return f"{self.character} ({j})"
