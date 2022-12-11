from django.db import models
from tourney.models import Team

pronoun_choices = [
    ('he', 'he/him'),
    ('she', 'she/her'),
    ('they','they/them'),
    ('ze','ze/hir')
]

class Competitor(models.Model):
    name = models.CharField(max_length=30)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='competitors',related_query_name='competitor')
    pronouns = models.CharField(max_length=20, choices=pronoun_choices, null=True, blank=True)

    def __str__(self):
        if self.pronouns == None:
            return self.name
        else:
            for (i, j) in pronoun_choices:
                if i == self.pronouns:
                    return f"{self.name} ({j})"

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
                if ballot.judge != ballot.round.extra_judge:
                    if ballot.round.p_team == self.team:
                        p_total += v
                    else:
                        d_total += v
        tournament = self.team.user.tournament
        if tournament.individual_award_rank_plus_record:
            p_total += self.team.p_ballot()
            d_total += self.team.d_ballot()
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
                if ballot.judge != ballot.round.extra_judge:
                    if ballot.round.p_team == self.team:
                        p_total += v
                    else:
                        d_total += v
        tournament = self.team.user.tournament
        if tournament.individual_award_rank_plus_record:
            p_total += self.team.p_ballot()
            d_total += self.team.d_ballot()
        return [p_total, d_total]

    def __lt__(self, other):
        return self.id < other.id

    class Meta:
        ordering = ['id']