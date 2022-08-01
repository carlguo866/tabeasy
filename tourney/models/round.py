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
    @property
    def judges(self):
        if self.extra_judge != None:
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
                if round != self and round.d_team == self.d_team:
                    errors.append(f"{self.p_team} and {self.d_team} played each other before")
            for round in self.p_team.d_rounds.all():
                if round != self and round.p_team == self.d_team:
                    errors.append(f"{self.p_team} and {self.d_team} played each other before")

        if self.pairing.final_submit:
            if self.presiding_judge == self.scoring_judge:
                errors.append('assigning one judge for two roles')
            if self.presiding_judge.preside == 0:
                errors.append(f'{self.presiding_judge} can\'t preside')

            for judge in self.judges:
                if judge != None:
                    if not judge.get_availability(self.pairing.round_num):
                        errors.append(f"{judge} is not available for Round {self.pairing.round_num}")
                    #check conflict
                    for team in self.teams:
                        if team in judge.conflicts.all():
                            errors.append(f"{judge} conflicted with p_team {team}")

                    #check if judged
                    judged = None
                    for round in judge.rounds:
                        if round != self:
                            if judged == None:
                                judged = Team.objects.filter(pk=round.p_team.pk)
                            else:
                                judged |= Team.objects.filter(pk=round.p_team.pk)
                            judged |= Team.objects.filter(pk=round.d_team.pk)
                    if judged != None:
                        for team in self.teams:
                            if team in judged:
                                errors.append(f"{judge} has judged p_team {team}")

                    # #check if assigned in another division
                    pairings = Pairing.objects.filter(round_num=self.pairing.round_num)
                    if pairings.exists():
                        for pairing in pairings.all():
                            if pairing != self.pairing:
                                for round in pairing.rounds.all():
                                    if judge in [round.presiding_judge,round.scoring_judge]:
                                        errors.append(f"{judge} already assigned in {pairing.division}")

        if errors != []:
            raise ValidationError(errors)


    def save(self):
        is_new = self.id is None
        super(Round, self).save()
        if is_new:
            CaptainsMeeting.objects.create(round=self)
        if self.pairing.final_submit and not self.pairing.publish:
            if Ballot.objects.filter(round=self).exists():
                Ballot.objects.filter(round=self).delete() #there is definitely a better way to do this
            Ballot.objects.create(round=self, judge=self.presiding_judge)
            Ballot.objects.create(round=self, judge=self.scoring_judge)
            if self.extra_judge != None:
                Ballot.objects.create(round=self, judge=self.extra_judge)


