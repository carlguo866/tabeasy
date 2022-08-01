from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

from tourney.models.team import Team

class Judge(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE,
                                primary_key=True, related_name='judge')
    conflicts = models.ManyToManyField(
        Team,
        blank=True
    )

    judge_friends = models.ManyToManyField(
        'self',
        blank=True
    )
    preside_choices = [
        (0, 'No'),
        (1, 'Yes'),
        (2, 'Can if needed'),
    ]

    preside = models.IntegerField(choices=preside_choices, default=0)
    available_round1 = models.BooleanField(default=False)
    available_round2 = models.BooleanField(default=False)
    available_round3 = models.BooleanField(default=False)
    available_round4 = models.BooleanField(default=False)
    available_round5 = models.BooleanField(default=False)

    def get_availability(self, round_num):
        return getattr(self, f"available_round{round_num}")


    def get_preside_preference(self):
        return self.preside_choices[self.preside][1]

    @property
    def rounds(self):
        return self.presiding_rounds.all().union(self.scoring_rounds.all())


    def __str__(self):
        return self.user.__str__()