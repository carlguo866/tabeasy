import functools

from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

# @functools.total_ordering
class Team(models.Model):
    team_id = models.IntegerField(primary_key=True, help_text="enter integer only")
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='team', null=True,blank=True)

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
                        if ballot.judge != round.extra_judge:
                            ballots.append(ballot)
        return ballots

    def p_ballot(self):
        if self.p_rounds.count() > 0:
            return sum([ballot.p_ballot for round in self.p_rounds.all()
                        for ballot in round.ballots.all() if ballot.judge != round.extra_judge
                        and ballot.round.pairing.round_num != 5])
        else:
            return 0

    def d_ballot(self):
        if self.d_rounds.count() > 0:
            return sum([ballot.d_ballot for round in self.d_rounds.all()
                        for ballot in round.ballots.all() if ballot.judge != round.extra_judge
                        and ballot.round.pairing.round_num != 5])
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
        if self.d_rounds.count() > 0 or self.p_rounds.count() > 0:
            p_pd = sum([ballot.p_pd for round in self.p_rounds.all()
                        for ballot in round.ballots.all() if ballot.judge != round.extra_judge
                        and ballot.round.pairing.round_num != 5])
            d_pd = sum([ballot.d_pd for round in self.d_rounds.all()
                        for ballot in round.ballots.all() if ballot.judge != round.extra_judge
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

class TeamMember(models.Model):
    name = models.CharField(max_length=30)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='members',related_query_name='member')

    def __str__(self):
        return self.name

    def att_individual_score(self):
        p_total = 0
        d_total = 0
        dict = {
            self.att_rank_1.all(): 5,
            self.att_rank_2.all(): 4,
            self.att_rank_3.all(): 3,
            self.att_rank_4.all(): 2,
        }
        for k, v in dict.items():
            for ballot in k:
                if ballot.round.p_team == self.team:
                    p_total += v
                else:
                    d_total += v
        return [p_total, d_total]

    def wit_individual_score(self):
        p_total = 0
        d_total = 0
        dict = {
            self.wit_rank_1.all(): 5,
            self.wit_rank_2.all(): 4,
            self.wit_rank_3.all(): 3,
            self.wit_rank_4.all(): 2,
        }
        for k, v in dict.items():
            for ballot in k:
                if ballot.round.p_team == self.team:
                    p_total += v
                else:
                    d_total += v
        return [p_total, d_total]

    def __lt__(self, other):
        return self.id < other.id

    class Meta:
        ordering = ['id']


class NonReversibleForeignKey(models.ForeignKey):
    _relation_counter = 0

    @classmethod
    def generate_related_name(cls):
        cls._relation_counter += 1
        return "anonymous_relation_%s" % cls._relation_counter
    #
    # def contribute_to_related_class(self, cls, related):
    #     self.name = NonReversibleForeignKey.generate_related_name()
    #     return super(NonReversibleForeignKey, self).contribute_to_related_class(cls, related)
