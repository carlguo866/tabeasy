from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

from tourney.models.judge import Judge
from tourney.models.round import Round
from tourney.models.team import Team


class Ballot(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE,
                              related_name='ballots',
                              related_query_name='ballot')
    judge = models.ForeignKey(Judge, on_delete=models.CASCADE,
                              related_name='ballots',
                              related_query_name='ballot')
    # @property
    # def p_roster_choices(self):
    #     return [(i, i) for i in self.p_team.team_roster]
    # @property
    # def d_roster_choices(self):
    #     return [(i, i) for i in self.d_team.team_roster]

    #Scores
    # p_open_name = models.CharField(max_length=20, choices=p_roster_choices(), null=True)
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

    att_ranks = ArrayField(
        models.CharField(max_length=20),
        size=4,
        null=True,
        blank=True
    )

    wit_ranks = ArrayField(
        models.CharField(max_length=20),
        size=4,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.judge.user.username} Ballot {self.id}"

    def calculate_win(self):
        assert(not None in set([self.p_open, self.p_wit1_att_direct, self.p_wit1_wit_direct, self.p_wit1_wit_cross,
                        self.p_wit2_att_direct, self.p_wit2_wit_direct, self.p_wit2_wit_cross ,
                        self.p_wit3_att_direct, self.p_wit3_wit_direct, self.p_wit3_wit_cross,
                        self.d_wit1_att_cross , self.d_wit2_att_cross , self.d_wit3_att_cross,
                        self.p_close])), 'None in the p_scores cant run calculate_win()'
        p_total_score = self.p_open + self.p_wit1_att_direct + self.p_wit1_wit_direct + self.p_wit1_wit_cross + \
                        self.p_wit2_att_direct + self.p_wit2_wit_direct + self.p_wit2_wit_cross + \
                        self.p_wit3_att_direct + self.p_wit3_wit_direct + self.p_wit3_wit_cross + \
                        self.d_wit1_att_cross + self.d_wit2_att_cross + self.d_wit3_att_cross + \
                        self.p_close
        assert(not None in set([
            self.d_open, self.d_wit1_att_direct, self.d_wit1_wit_direct, self.d_wit1_wit_cross,
            self.d_wit2_att_direct,  self.d_wit2_wit_direct,  self.d_wit2_wit_cross,
            self.d_wit3_att_direct,  self.d_wit3_wit_direct,  self.d_wit3_wit_cross,
            self.p_wit1_att_cross , self.p_wit2_att_cross + self.p_wit3_att_cross ,
            self.d_close
        ])), 'None in the d_scores cant run calculate_win()'
        d_total_score = self.d_open + self.d_wit1_att_direct + self.d_wit1_wit_direct + self.d_wit1_wit_cross + \
                        self.d_wit2_att_direct + self.d_wit2_wit_direct + self.d_wit2_wit_cross + \
                        self.d_wit3_att_direct + self.d_wit3_wit_direct + self.d_wit3_wit_cross + \
                        self.p_wit1_att_cross + self.p_wit2_att_cross + self.p_wit3_att_cross + \
                        self.d_close
        return p_total_score - d_total_score

    def p_result(self):
        pd = self.calculate_win()
        if pd != 0:
            return int(pd > 0), pd
        else:
            return 0.5, pd

    def d_result(self):
        pd = self.calculate_win()
        if pd != 0:
            return int(pd < 0), pd
        else:
            return 0.5, pd

    class Meta:
        unique_together = ['round', 'judge']
