from django.db import models

from submission.models.captains_meeting import CaptainsMeeting
from tourney.models import Tournament

pronoun_choices = [
    ('he', 'He/Him'),
    ('she', 'She/Her'),
    ('they','They/Them'),
    ('ze','Ze/Hir')
]
side_choices = [
    ('p', 'P'),
    ('d', 'D'),
    ('other','Other'),
]

class Character(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='characters',
                                    related_query_name='character', null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    side = models.CharField(max_length=5, choices=side_choices, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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