from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# Create your models here
from django_better_admin_arrayfield.models.fields import ArrayField

from tourney.models.judge import Judge
from tourney.models.team import Team


class Pairing(models.Model):
    id = models.BigAutoField(primary_key=True)
    division_choices = [('Disney', 'Disney'), ('Universal', 'Universal')]
    division = models.CharField(
        max_length=100,
        choices=division_choices
    )
    round_num = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # div_1 = ArrayField(
    #     ArrayField(
    #         models.CharField(max_length=30, null=True),
    #         size=6,
    #         null=True
    #     ),
    #     null=True,
    #     blank=True
    # # )
    #rounds = models.OneToManyField(Round, related_name='rounds', related_query_name='round')
    # div_1_team_1 = models.CharField(max_length=30)

    def __str__(self):
        return f'Round {self.round_num}'

    def clean(self):
        super().clean()
        existing_teams = []
        existing_judges = []
        for pairing_item in self.rounds.all():
            print(pairing_item)
            print(existing_teams)
            if pairing_item.p_team in existing_teams:
                raise ValidationError(f'repeated a team {pairing_item.p_team}')
            elif pairing_item.d_team in existing_teams:
                raise ValidationError(f'repeated a team {pairing_item.d_team}')
            else:
                existing_teams.extend([pairing_item.p_team, pairing_item.d_team])

            if pairing_item.judge_1 in existing_judges :
                raise ValidationError(f'repeated a judge {pairing_item.judge_1}')
            elif pairing_item.judge_2 in existing_judges:
                raise ValidationError(f'repeated a judge {pairing_item.judge_2}')
            else:
                existing_judges.extend([pairing_item.judge_1, pairing_item.judge_2])


class Round(models.Model):
    id = models.AutoField(primary_key=True)
    pairing = models.ForeignKey(Pairing, on_delete=models.CASCADE, related_name='rounds', related_query_name='round', null=True)
    courtroom = models.CharField(max_length=1, null=True)
    p_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='p_teams',
                               related_query_name='p_team', null=True)
    d_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='d_teams',
                               related_query_name='d_team', null=True)
    judge_1 = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name='pairing1s',
                               related_query_name='pairing1', null=True)
    judge_2 = models.ForeignKey(Judge, on_delete=models.CASCADE, related_name='pairing2s',
                                related_query_name='pairing2', null=True)

    def __str__(self):
        return f'Round {self.pairing.round_num} Courtroom {self.courtroom.upper()}'

    def clean(self):
        """check that word and characters do not mismatch in chinese & pinyin"""
        super().clean()
        if self.judge_1 == self.judge_2:
            raise ValidationError('cant have the same two judges')

        if self.p_team == self.d_team:
            raise ValidationError('one team cant compete against itself')