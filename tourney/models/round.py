from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# Create your models here
from django_better_admin_arrayfield.models.fields import ArrayField

from tourney.models import Ballot
from tourney.models.captains_meeting import CaptainsMeeting
from tourney.models.team import Team, TeamMember


class Pairing(models.Model):
    division_choices = [('Disney', 'Disney'), ('Universal', 'Universal')]
    division = models.CharField(
        max_length=100,
        choices=division_choices
    )
    round_num = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    team_submit = models.BooleanField(default=False)
    final_submit = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)

    def get_rounds(self):
        return self.rounds.order_by('courtroom')


    class Meta:
        unique_together = ('division', 'round_num',)

    def __str__(self):
        return f'Round {self.round_num} {self.division}'

class Round(models.Model):
    pairing = models.ForeignKey(Pairing, on_delete=models.CASCADE, related_name='rounds', related_query_name='round', null=True)
    courtroom = models.CharField(max_length=1, null=True)
    p_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='p_rounds',
                               related_query_name='p_round', null=True)
    d_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='d_rounds',
                               related_query_name='d_round', null=True)
    presiding_judge = models.ForeignKey('Judge', on_delete=models.CASCADE, related_name='presiding_rounds',
                                    related_query_name='presiding_round', null=True)
    scoring_judge = models.ForeignKey('Judge', on_delete=models.CASCADE, related_name='scoring_rounds',
                                    related_query_name='scoring_round', null=True)
    extra_judge = models.ForeignKey('Judge', on_delete=models.CASCADE, related_name='extra_rounds',
                                      related_query_name='extra_round', null=True, blank=True)
    judge_panel = models.ManyToManyField('Judge', related_name='final_rounds', related_query_name='final_round',
                                         null=True, blank=True)

    @property
    def judges(self):
        if self.judge_panel.count() > 0:
            return [self.presiding_judge, self.scoring_judge] + [judge for judge in self.judge_panel.all()]
        elif self.extra_judge != None:
            return [self.presiding_judge, self.scoring_judge, self.extra_judge]
        else:
            return [self.presiding_judge, self.scoring_judge]

    @property
    def teams(self):
        return [self.p_team, self.d_team]

    def __str__(self):
        return f'Round {self.pairing.round_num} Courtroom {self.courtroom}'


    def clean(self):
        super().clean()
        errors = []

        if self.pairing.team_submit or self.pairing.final_submit:
            if self.p_team == self.d_team:
                errors.append('one team cant compete against itself')
            if self.p_team.next_side(self.pairing.round_num) == 'd':
                errors.append(f"{self.p_team} is supposed to play d this round")
            if self.d_team.next_side(self.pairing.round_num) == 'p':
                errors.append(f"{self.d_team} is supposed to play p this round")
            for round in self.p_team.p_rounds.all():
                if round != self and round.pairing != self.pairing and round.d_team == self.d_team:
                    errors.append(f"{self.p_team} and {self.d_team} played each other before")
            for round in self.p_team.d_rounds.all():
                if round != self and round.pairing != self.pairing and round.p_team == self.d_team:
                    errors.append(f"{self.p_team} and {self.d_team} played each other before")

        if self.pairing.final_submit:

            if self.presiding_judge.preside == 0:
                errors.append(f'{self.presiding_judge} can\'t preside')
            if len(self.judges) != len(set(self.judges)):
                errors.append(f'assigning one judge for two roles in {self}')


            for judge in self.judges:
                if judge != None:
                    if not judge.get_availability(self.pairing.round_num):
                        errors.append(f"{judge} is not available for Round {self.pairing.round_num}")
                    #check conflict
                    for team in self.teams:
                        if team in judge.conflicts.all():
                            errors.append(f"{judge} conflicted with team {team}")

                    #check if judged
                    judged = judge.judged(self.pairing.round_num)
                    if judged != []:
                        for team in self.teams:
                            if team in judged:
                                errors.append(f"{judge} has judged team {team}")

        if errors != []:
            raise ValidationError(errors)


    def save(self):
        is_new = self.id is None
        super(Round, self).save()
        if is_new:
            CaptainsMeeting.objects.create(round=self)
        # if self.pairing.final_submit and not self.pairing.publish:
        #     if not Ballot.objects.filter(round=self).exists():
        #         for judge in self.judges:
        #             Ballot.objects.create(round=self, judge=judge)
        #     else:
        #         for judge in self.judges:
        #             if not Ballot.objects.filter(round=self, judge=judge).exists():
        #                 Ballot.objects.create(round=self, judge=judge)
        #         for ballot in Ballot.objects.filter(round=self).all():
        #             if ballot.judge not in self.judges:
        #                 Ballot.objects.filter(round=self, judge=ballot.judge).delete()



