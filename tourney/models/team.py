import functools

from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

# @functools.total_ordering
class Team(models.Model):
    team_id = models.BigAutoField(primary_key=True, help_text="enter integer only")
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='team', null=True,blank=True)

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
            queryset = [round for round in self.p_rounds.all()] + [round for round in self.d_rounds.all()]
            return sorted(queryset, key=lambda x: x.pairing.round_num)
        elif self.p_rounds.exists():
            return self.p_rounds.order_by('pairing__round_num').all()
        elif self.d_rounds.exists():
            return self.d_rounds.order_by('pairing__round_num').all()
        else:
            return None

    def published_ballots(self):
        ballots = []
        if self.rounds() != None:
            for round in self.rounds():
                if round.pairing.publish:
                    for ballot in round.ballots.all():
                        if self.user.tournament.judges == 3 or ballot.judge != round.extra_judge:
                            ballots.append(ballot)
        return ballots

    def p_ballot(self):
        if self.p_rounds.count() > 0:
            if self.user.tournament.judges == 1:
                return sum([ballot.p_ballot for round in self.p_rounds.all()
                            for ballot in round.ballots.all() if ballot.judge == round.presiding_judge])
            else:
                return sum([ballot.p_ballot for round in self.p_rounds.all()
                        for ballot in round.ballots.all() if self.user.tournament.judges == 3  or \
                            ballot.judge != round.extra_judge
                        and ballot.round.pairing.round_num != 5])
        else:
            return 0

    def d_ballot(self):
        if self.d_rounds.count() > 0:
            if self.user.tournament.judges == 1:
                return sum([ballot.d_ballot for round in self.d_rounds.all()
                        for ballot in round.ballots.all() if ballot.judge == round.presiding_judge])
            else:
                return sum([ballot.d_ballot for round in self.d_rounds.all()
                        for ballot in round.ballots.all() if self.user.tournament.judges == 3  or \
                            ballot.judge != round.extra_judge
                        and ballot.round.pairing.round_num != 5])
        else:
            return 0

    def total_ballots(self):
        # self.total_ballots = self.p_ballot() + self.d_ballot()
        return self.p_ballot() + self.d_ballot()

    def total_cs(self):
        cs = 0
        for p_round in self.p_rounds.all():
            if p_round.pairing.round_num != 5:
                cs += p_round.d_team.total_ballots()
        for d_round in self.d_rounds.all():
            if d_round.pairing.round_num != 5:
                cs += d_round.p_team.total_ballots()
        return cs

    def total_pd(self):
        if self.d_rounds.count() > 0 or self.p_rounds.count() > 0:
            p_pd = sum([ballot.p_pd for round in self.p_rounds.all()
                        for ballot in round.ballots.all() if self.user.tournament.judges == 3  or \
                            ballot.judge != round.extra_judge
                        and ballot.round.pairing.round_num != 5])
            d_pd = sum([ballot.d_pd for round in self.d_rounds.all()
                        for ballot in round.ballots.all() if self.user.tournament.judges == 3  or \
                            ballot.judge != round.extra_judge
                        and ballot.round.pairing.round_num != 5])
            return p_pd + d_pd
        else:
            return 0

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

    # def __lt__(self, other):
    #     if self.total_ballots() == other.total_ballots():
    #         if self.total_cs() == other.total_cs():
    #             return self.total_pd() - other.total_pd()
    #         else:
    #             return self.total_cs() - other.total_cs()
    #     else:
    #         return self.total_ballots() - other.total_ballots()




