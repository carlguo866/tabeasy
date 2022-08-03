from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

from tourney.models.team import Team, TeamMember


class Ballot(models.Model):
    round = models.ForeignKey('Round', on_delete=models.CASCADE,
                              related_name='ballots',
                              related_query_name='ballot')
    judge = models.ForeignKey('Judge', on_delete=models.CASCADE,
                              related_name='ballots',
                              related_query_name='ballot')

    #Scores
    p_open = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_open_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_open = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_open_comment = models.TextField(max_length=5000,null=True, blank=True)

    p_wit1_wit_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit1_wit_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit1_att_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit1_att_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                           help_text='this is for d!',null=True)
    p_wit1_wit_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit1_wit_cross_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit1_att_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit1_att_cross_comment = models.TextField(max_length=5000,null=True, blank=True)

    p_wit2_wit_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit2_wit_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit2_att_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit2_att_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                           help_text='this is for d!',null=True)
    p_wit2_wit_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit2_wit_cross_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit2_att_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit2_att_cross_comment = models.TextField(max_length=5000,null=True, blank=True)

    p_wit3_wit_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit3_wit_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit3_att_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_wit3_att_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                           help_text='this is for d!',null=True)
    p_wit3_wit_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit3_wit_cross_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit3_att_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    p_wit3_att_cross_comment = models.TextField(max_length=5000,null=True, blank=True)

    d_wit1_wit_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit1_wit_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit1_att_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit1_att_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                           help_text='this is for p!',null=True)
    d_wit1_wit_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit1_wit_cross_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit1_att_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit1_att_cross_comment = models.TextField(max_length=5000,null=True, blank=True)

    d_wit2_wit_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit2_wit_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit2_att_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit2_att_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                           help_text='this is for p!',null=True)
    d_wit2_wit_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit2_wit_cross_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit2_att_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit2_att_cross_comment = models.TextField(max_length=5000,null=True, blank=True)

    d_wit3_wit_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit3_wit_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit3_att_direct = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_wit3_att_cross = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],
                                           help_text='this is for p!',null=True)
    d_wit3_wit_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit3_wit_cross_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit3_att_direct_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_wit3_att_cross_comment = models.TextField(max_length=5000,null=True, blank=True)


    p_close = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    p_close_comment = models.TextField(max_length=5000,null=True, blank=True)
    d_close = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)],null=True)
    d_close_comment = models.TextField(max_length=5000,null=True, blank=True)

    att_rank_1 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='att_rank_1',
                                   related_name='att_rank_1',null=True)
    att_rank_2 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='att_rank_2',
                                   related_name='att_rank_2',null=True)
    att_rank_3 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='att_rank_3',
                                   related_name='att_rank_3',null=True)
    att_rank_4 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='att_rank_4',
                                   related_name='att_rank_4',null=True)

    wit_rank_1 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='wit_rank_1',
                                   related_name='wit_rank_1',null=True)
    wit_rank_2 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='wit_rank_2',
                                   related_name='wit_rank_2',null=True)
    wit_rank_3 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='wit_rank_3',
                                   related_name='wit_rank_3',null=True)
    wit_rank_4 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_query_name='wit_rank_4',
                                   related_name='wit_rank_4',null=True)

    submit = models.BooleanField(default=False, help_text='Submit')

    def att_ranks(self):
        return [self.att_rank_1, self.att_rank_2, self.att_rank_3, self.att_rank_4]

    def wit_ranks(self):
        return [self.wit_rank_1, self.wit_rank_2, self.wit_rank_3, self.wit_rank_4]


    def __str__(self):
        return f"Round {self.round.pairing.round_num} {self.judge}"

    def p_total_score(self):
        if self.submit:
            assert(not None in {self.p_open, self.p_wit1_att_direct, self.p_wit1_wit_direct, self.p_wit1_wit_cross,
                                self.p_wit2_att_direct, self.p_wit2_wit_direct, self.p_wit2_wit_cross,
                                self.p_wit3_att_direct, self.p_wit3_wit_direct, self.p_wit3_wit_cross,
                                self.d_wit1_att_cross, self.d_wit2_att_cross, self.d_wit3_att_cross,
                                self.p_close}), 'None in the p_scores cant run calculate_win()'
            p_total_score = self.p_open + self.p_wit1_att_direct + self.p_wit1_wit_direct + self.p_wit1_wit_cross + \
                            self.p_wit2_att_direct + self.p_wit2_wit_direct + self.p_wit2_wit_cross + \
                            self.p_wit3_att_direct + self.p_wit3_wit_direct + self.p_wit3_wit_cross + \
                            self.d_wit1_att_cross + self.d_wit2_att_cross + self.d_wit3_att_cross + \
                            self.p_close
            return p_total_score
        else:
            return 0

    def d_total_score(self):
        if self.submit:
            assert (not None in {self.d_open, self.d_wit1_att_direct, self.d_wit1_wit_direct, self.d_wit1_wit_cross,
                                 self.d_wit2_att_direct, self.d_wit2_wit_direct, self.d_wit2_wit_cross,
                                 self.d_wit3_att_direct, self.d_wit3_wit_direct, self.d_wit3_wit_cross,
                                 self.p_wit1_att_cross, self.p_wit2_att_cross + self.p_wit3_att_cross,
                                 self.d_close}), 'None in the d_scores cant run calculate_win()'
            d_total_score = self.d_open + self.d_wit1_att_direct + self.d_wit1_wit_direct + self.d_wit1_wit_cross + \
                            self.d_wit2_att_direct + self.d_wit2_wit_direct + self.d_wit2_wit_cross + \
                            self.d_wit3_att_direct + self.d_wit3_wit_direct + self.d_wit3_wit_cross + \
                            self.p_wit1_att_cross + self.p_wit2_att_cross + self.p_wit3_att_cross + \
                            self.d_close
            return d_total_score
        else:
            return 0

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
        if self.submit:
            if len(self.att_ranks()) != len(set(self.att_ranks())):
                errors.append('You can only rank each attorney once')
            if len(self.wit_ranks()) != len(set(self.wit_ranks())):
                errors.append('You can only rank each witness once')

        if errors != []:
            raise ValidationError(errors)
