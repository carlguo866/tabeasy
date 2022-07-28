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



    def __str__(self):
        return f'Round {self.pairing.round_num} Courtroom {self.courtroom}'


    def clean(self):
        super().clean()
        errors = []
        if self.presiding_judge.preside == 0:
            errors.append(f'{self.presiding_judge} can\'t preside')
        if errors != []:
            raise ValidationError(errors)


    def save(self):
        is_new = self.id is None
        super(Round, self).save()
        if is_new:
            CaptainsMeeting.objects.create(round=self)
        if Ballot.objects.filter(round=self).exists():
            Ballot.objects.filter(round=self).delete()
        Ballot.objects.create(round=self, judge=self.presiding_judge)
        Ballot.objects.create(round=self, judge=self.scoring_judge)
        if self.extra_judge != None:
            Ballot.objects.create(round=self, judge=self.extra_judge)


