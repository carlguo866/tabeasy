
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

from tourney.models.judge import Judge
from tourney.models.round import Round
from tourney.models.team import Team
from tourney.models.competitor import Competitor
import uuid


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "ballot_{0}/{1}".format(instance.id, filename)


class Ballot(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE,
                              related_name='ballots',
                              related_query_name='ballot')
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE,
                              related_name='ballots',
                              related_query_name='ballot')

    att_rank_1 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='att_rank_1',
                                   related_name='att_rank_1', null=True)
    att_rank_2 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='att_rank_2',
                                   related_name='att_rank_2', null=True)
    att_rank_3 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='att_rank_3',
                                   related_name='att_rank_3', null=True)
    att_rank_4 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='att_rank_4',
                                   related_name='att_rank_4', null=True)

    wit_rank_1 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='wit_rank_1',
                                   related_name='wit_rank_1', null=True)
    wit_rank_2 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='wit_rank_2',
                                   related_name='wit_rank_2', null=True)
    wit_rank_3 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='wit_rank_3',
                                   related_name='wit_rank_3', null=True)
    wit_rank_4 = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_query_name='wit_rank_4',
                                   related_name='wit_rank_4', null=True)
    upload = models.FileField(upload_to=user_directory_path, null=True)
    submit = models.BooleanField(default=False, help_text='Submit')

    def att_ranks(self):
        return [self.att_rank_1, self.att_rank_2, self.att_rank_3, self.att_rank_4]

    def wit_ranks(self):
        return [self.wit_rank_1, self.wit_rank_2, self.wit_rank_3, self.wit_rank_4]

    def __str__(self):
        return f"Round {self.round.pairing.round_num} {self.judge}"

    def p_total_score(self):
        p_total_score = 0
        scores = [ballot_section.score for ballot_section in self.sections.filter(
            subsection__side='P').all()]
        for score in scores:
            if score:
                p_total_score += score
        return p_total_score

    def d_total_score(self):
        d_total_score = 0
        scores = [ballot_section.score for ballot_section in self.sections.filter(
            subsection__side='D').all()]
        for score in scores:
            if score:
                d_total_score += score
        return d_total_score

    def calculate_win(self):
        if self.submit:
            return self.p_total_score() - self.d_total_score()
        else:
            return 0

    @property
    def p_result(self):
        if self.submit:
            pd = self.calculate_win()
            if pd != 0:
                return int(pd > 0), pd
            else:
                return 0.5, pd
        else:
            return 0, 0

    @property
    def p_pd(self):
        return self.p_result[1]

    @property
    def p_ballot(self):
        return self.p_result[0]

    @property
    def d_result(self):
        if self.submit:
            pd = self.calculate_win()
            if pd != 0:
                return int(pd < 0), -pd
            else:
                return 0.5, -pd
        else:
            return 0, 0

    @property
    def d_pd(self):
        return self.d_result[1]

    @property
    def d_ballot(self):
        return self.d_result[0]

    class Meta:
        unique_together = ['round', 'judge']

    def clean(self):
        super().clean()
        errors = []
        if not self.round.pairing.round_num == 5 and self.submit:
            if len(self.att_ranks()) != len(set(self.att_ranks())):
                errors.append('You can only rank each attorney once')
            if len(self.wit_ranks()) != len(set(self.wit_ranks())):
                errors.append('You can only rank each witness once')

        if errors != []:
            raise ValidationError(errors)

        self.round.p_team.calc_p_ballots()
        self.round.p_team.calc_d_ballots()
        self.round.p_team.calc_total_ballots()
        self.round.d_team.calc_p_ballots()
        self.round.d_team.calc_d_ballots()
        self.round.d_team.calc_total_ballots()

        self.round.p_team.calc_total_cs()
        self.round.p_team.calc_total_pd()
        self.round.d_team.calc_total_cs()
        self.round.d_team.calc_total_pd()

        for att in [self.att_rank_1, self.att_rank_2, self.att_rank_3, self.att_rank_4]:
            if att:
                att.calc_att_individual_score()

        for wit in [self.wit_rank_1, self.wit_rank_2, self.wit_rank_3, self.wit_rank_4]:
            if wit:
                wit.calc_wit_individual_score()
