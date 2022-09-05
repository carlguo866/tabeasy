from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField

from tourney.models.team import Team
from tourney.models.tournament import Tournament


class Judge(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE,
                                primary_key=True, related_name='judge')
    conflicts = models.ManyToManyField(
        Team,
        blank=True
    )

    judge_friends = models.ManyToManyField(
        'self',
        blank=True
    )
    preside_choices = [
        (0, 'No'),
        (1, 'Yes'),
        (2, 'Can if needed'),
    ]

    preside = models.IntegerField(choices=preside_choices, default=0)
    available_round1 = models.BooleanField(default=False)
    available_round2 = models.BooleanField(default=False)
    available_round3 = models.BooleanField(default=False)
    available_round4 = models.BooleanField(default=False)
    available_round5 = models.BooleanField(default=False)

    checkin = models.BooleanField(default=False)

    def get_availability(self, round_num):
        return getattr(self, f"available_round{round_num}")

    def get_preside_preference(self):
        return self.preside_choices[self.preside][1]

    def is_assigned(self, round_num):
        assigned = False
        for round in self.rounds:
            if round.pairing.round_num == round_num:
                assigned = True
        return assigned


    @property
    def rounds(self):
        queryset = [round for round in self.presiding_rounds.all()] + [round for round in self.scoring_rounds.all()]\
                    +[round for round in self.extra_rounds.all()]
        return sorted(queryset, key=lambda x: x.pairing.round_num)


    def judged(self, round_num):
        judged = []
        for round in self.rounds:
            if round == None or round.p_team == None or round.d_team == None:
                continue
            if round.pairing.round_num != round_num:
                judged += [Team.objects.get(pk=round.p_team.pk),Team.objects.get(pk=round.d_team.pk)]
        return judged


    def __str__(self):
        return self.user.__str__()

experience_description_choices = [
    ('hs', 'I am a former High School Mock Trial Competitor'),
    ('college', 'I am a current or former College Mock Trial Competitor'),
    ('ls', 'I am a current or former Law School Mock Trial Competitor'),
]


judged_rounds_choices = [
    (1,'I have judged 1-2 Mock Trial Competitions in the past'),
    (2,'I have judged 3-5 Mock Trial Competitions in the past'),
    (3,'I have judged 5 or more Mock Trial Competitions in the past'),
]

class Paradigm(models.Model):
    judge = models.OneToOneField(Judge, on_delete=models.CASCADE,
                                primary_key=True, related_name='paradigm')
    experience_years = models.DecimalField(default=1, max_digits=3, decimal_places=1, help_text='How many years of mock trial experience do you have?')
    experience_description = models.CharField(max_length=40, choices=experience_description_choices,
                                              help_text='Do you have any experience competing in high school, collegiate or law school mock trial competitions?')
    judged_rounds = models.IntegerField(choices=judged_rounds_choices,
                                        help_text='Do you have any experience judging high school, collegiate or law school mock trial competitions?')
    affiliations = models.CharField(max_length=200, null=True, blank=True)
    #scale On a scale of 1-10, I prefer mock trial attorneys who…
    comments = models.TextField(max_length=5000, null=True, blank=True)

role_choices = [
    ('att', 'Attorney'),
    ('wit', 'Witness')
]
class ParadigmPreference(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, related_name='paradigm_preferences',
                                   related_query_name='paradigm_preference', null=True)
    role = models.CharField(max_length=40, choices=role_choices)
    low_end = models.CharField(max_length=40, null=True, blank=True)
    high_end = models.CharField(max_length=40, null=True, blank=True)

class ParadigmPreferenceItem(models.Model):
    paradigm = models.ForeignKey(Paradigm, on_delete=models.CASCADE, related_name='preferences',
                                 related_query_name='preference_scale')
    paradigm_preference = models.ForeignKey(ParadigmPreference, on_delete=models.CASCADE, related_name='paradigm_preference_items',
                                   related_query_name='paradigm_preference_items', null=True)
    scale = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],default=5)



