from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

from submission.models.ballot import Ballot
from tourney.models.team import Team
from tourney.models.tournament import Tournament


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

    checkin = models.BooleanField(default=False)

    def get_availability(self, round_num):
        return getattr(self, f"available_round{round_num}")

    def get_preside_preference(self):
        return self.preside_choices[self.preside][1]

    def is_assigned(self, round_num):
        assigned = False
        for round in self.rounds:
            if round.pairing.round_num == round_num:
                assigned = True
        return assigned


    @property
    def rounds(self):
        queryset = [round for round in self.presiding_rounds.all()] + [round for round in self.scoring_rounds.all()]\
                    +[round for round in self.extra_rounds.all()]
        return sorted(queryset, key=lambda x: x.pairing.round_num)

    def available_ballots(self):
        return Ballot.objects.filter(round__pairing__tournament=self.tournament, judge=self)

    def judged(self, round_num):
        judged = []
        for round in self.rounds:
            if round == None or round.p_team == None or round.d_team == None:
                continue
            if round.pairing.round_num != round_num:
                judged += [Team.objects.get(pk=round.p_team.pk),Team.objects.get(pk=round.d_team.pk)]
        return judged


    def __str__(self):
        return self.user.__str__()
