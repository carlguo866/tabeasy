from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

from accounts.models import User


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True, help_text="enter integer only")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team', null=True,blank=True)

    team_name = models.CharField(
        max_length=100,
        default='PPMT Team',
        null=True
    )
    division_choices = [('Disney', 'Disney'), ('Universal', 'Universal')]
    division = models.CharField(
        max_length=100,
        choices=division_choices,
        null=True
    )
    school = models.CharField(
        max_length=100,
        default='placeholder',
        null=True
    )
    side_choices = [('P', 'Prosecution'), ('D', 'Defense')]
    sides = ArrayField(
        models.CharField(max_length=1, choices=side_choices),
        size=4,
        null=True,
        blank=True
    )

    # cs = ArrayField(
    #     models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True),
    #     size=4,
    #     null=True,
    #     blank=True
    # )
    # pd = ArrayField(
    #     models.IntegerField(null=True, blank=True),
    #     size=4,
    #     null=True,
    #     blank=True
    # )
    def __str__(self):
        return f"{self.team_name}"

    def p_ballot(self):
        if self.p_rounds.count() > 0:
            return sum([ballot[0] for ballot in round.ballots.all()
                        for round in self.p_rounds.all() ])
        else:
            return 0

    def d_ballot(self):
        if self.d_rounds.count() > 0:
            return sum([ballot[0] for ballot in round.ballots.all()
                        for round in self.d_rounds.all() ])
        else:
            return 0

    def total_ballots(self):
        return self.p_ballot() + self.d_ballot()

    def total_cs(self):
        cs = 0
        for p_round in self.p_rounds.all():
            cs += p_round.d_team.total_ballots()
        for d_round in self.d_rounds.all():
            cs += d_round.p_team.total_ballots()
        return cs

    def total_pd(self):
        if self.d_rounds.count() > 0 or self.p_rounds.count():
            return sum([ballot[1] for ballot in round.ballots.all()
                        for round in self.d_rounds.all()+self.p_rounds.all()])
        else:
            return 0

    def next_side(self):
        if self.p_rounds.count() == self.d_rounds.count():
            return 'both'
        elif self.p_rounds.count() > self.d_rounds.count():
            return 'd'
        else:
            return 'p'

class TeamMember(models.Model):
    name = models.CharField(max_length=30)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='members',related_query_name='member')

    @property
    def att_individual_score(self):
        total = 0
        dict = {
            self.att_rank_1: 5,
            self.att_rank_2: 4,
            self.att_rank_3: 3,
            self.att_rank_4: 2,
        }
        for k, v in dict:
            total += v*k.count()
        return total

    @property
    def wit_individual_score(self):
        total = 0
        dict = {
            self.wit_rank_1: 5,
            self.wit_rank_2: 4,
            self.wit_rank_3: 3,
            self.wit_rank_4: 2,
        }
        for k, v in dict:
            total += v*k.count()
        return total
