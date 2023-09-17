import functools

from django.core.exceptions import ValidationError
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

# @functools.total_ordering


class Team(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, primary_key=True,
                                related_name='team')
    p_ballots = models.FloatField(default=0)
    d_ballots = models.FloatField(default=0)
    total_ballots = models.FloatField(default=0)
    total_cs = models.FloatField(default=0)
    total_pd = models.FloatField(default=0)
    spirit_score = models.IntegerField(default=0)

    team_name = models.CharField(
        max_length=100,
        default='Team',
        null=True
    )
    division_choices = [('Disney', 'Disney'), ('Universal', 'Universal')]
    division = models.CharField(
        max_length=100,
        choices=division_choices,
        null=True,
        blank=True
    )
    school = models.CharField(
        max_length=100,
        default='',
        null=True
    )

    byebuster = models.BooleanField(default=False)

    def __str__(self):
        return self.user.__str__()

    def rounds(self):
        if self.p_rounds.exists() and self.d_rounds.exists():
            queryset = [round for round in self.p_rounds.all()] + \
                [round for round in self.d_rounds.all()]
            return sorted(queryset, key=lambda x: x.pairing.round_num)
        elif self.p_rounds.exists():
            return self.p_rounds.order_by('pairing__round_num').all()
        elif self.d_rounds.exists():
            return self.d_rounds.order_by('pairing__round_num').all()
        else:
            return None

    def round_opponent(self, round_num):
        p_rounds = self.p_rounds.filter(pairing__round_num=round_num)
        d_rounds = self.d_rounds.filter(pairing__round_num=round_num)
        if p_rounds.exists():
            return p_rounds.first().d_team
        elif d_rounds.exists():
            return d_rounds.first().p_team
        else:
            return None

    def opponents(self):
        teams = []
        for p_round in self.p_rounds.all():
            if p_round.pairing.round_num != 5:
                teams.append(p_round.d_team)
        for d_round in self.d_rounds.all():
            if d_round.pairing.round_num != 5:
                teams.append(d_round.p_team)
        return teams

    def published_ballots(self):
        ballots = []
        if self.rounds() != None:
            for round in self.rounds():
                if round.pairing.publish:
                    for ballot in round.ballots.all():
                        if self.user.tournament.judges == 3 or ballot.judge != round.extra_judge:
                            ballots.append(ballot)
        return ballots

    def calc_p_ballots(self):
        if self.p_rounds.count() > 0:
            if self.user.tournament.judges == 1:
                self.p_ballots = sum([ballot.p_ballot for round in self.p_rounds.all()
                                      for ballot in round.ballots.all() if ballot.judge == round.presiding_judge])
            else:
                self.p_ballots = sum([ballot.p_ballot for round in self.p_rounds.all()
                                      for ballot in round.ballots.all() if self.user.tournament.judges == 3 or
                                      ballot.judge != round.extra_judge
                                      and ballot.round.pairing.round_num != 5])
        else:
            self.p_ballots = 0

    def calc_d_ballots(self):
        if self.d_rounds.count() > 0:
            if self.user.tournament.judges == 1:
                self.d_ballots = sum([ballot.d_ballot for round in self.d_rounds.all()
                                      for ballot in round.ballots.all() if ballot.judge == round.presiding_judge])
            else:
                self.d_ballots = sum([ballot.d_ballot for round in self.d_rounds.all()
                                      for ballot in round.ballots.all() if self.user.tournament.judges == 3 or
                                      ballot.judge != round.extra_judge
                                      and ballot.round.pairing.round_num != 5])
        else:
            self.d_ballots = 0

    def calc_total_ballots(self):
        # self.total_ballots = self.p_ballot() + self.d_ballot()
        self.total_ballots = self.p_ballots + self.d_ballots

    def calc_total_cs(self):
        self.total_cs = sum(
            [opponent.total_ballots for opponent in self.opponents()])

    def calc_total_pd(self):
        if self.d_rounds.count() > 0 or self.p_rounds.count() > 0:
            p_pd = sum([ballot.p_pd for round in self.p_rounds.all()
                        for ballot in round.ballots.all()
                        if self.user.tournament.judges == 3 or
                        (self.user.tournament.judges == 2 and
                         ballot.judge != round.extra_judge) or
                        (self.user.tournament.judges == 1 and
                         ballot.judge == round.presiding_judge)
                        and ballot.round.pairing.round_num != 5])
            d_pd = sum([ballot.d_pd for round in self.d_rounds.all()
                        for ballot in round.ballots.all()
                        if self.user.tournament.judges == 3 or
                        (self.user.tournament.judges == 2 and
                         ballot.judge != round.extra_judge) or
                        (self.user.tournament.judges == 1 and
                         ballot.judge == round.presiding_judge)
                        and ballot.round.pairing.round_num != 5])
            self.total_pd = p_pd + d_pd
        else:
            self.total_pd = 0

    def calc_spirit_score(self):
        spirit_score = 0
        for i in range(3):
            opponent = self.round_opponent(i+1)
            if opponent and opponent.spirit and opponent.spirit.submit:
                spirit_score += opponent.spirit.get_score(i+1)
        self.spirit_score = spirit_score

    def current_rounds(self):
        return self.p_rounds.count() + self.d_rounds.count()

    def next_side(self, round_num):
        if self.current_rounds() == round_num:
            return 'good'
        elif round_num % 2 == 1:
            return 'both'
        else:
            for p_round in self.p_rounds.all():
                if p_round.pairing.round_num == round_num-1:
                    return 'd'
            for d_round in self.d_rounds.all():
                if d_round.pairing.round_num == round_num-1:
                    return 'p'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calc_p_ballots()
        self.calc_d_ballots()
        self.calc_total_ballots()
        self.calc_total_cs()
        self.calc_total_pd()
        self.calc_spirit_score()
        for competitor in self.competitors.all():
            competitor.save()
        super().save(*args, **kwargs)

    # def __lt__(self, other):
    #     if self.total_ballots() == other.total_ballots():
    #         if self.total_cs() == other.total_cs():
    #             return self.total_pd() - other.total_pd()
    #         else:
    #             return self.total_cs() - other.total_cs()
    #     else:
    #         return self.total_ballots() - other.total_ballots()
