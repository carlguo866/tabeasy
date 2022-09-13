from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from array_field_select.fields import ArrayField

experience_description_choices = [
    ('hs', 'I am a former High School Mock Trial Competitor'),
    ('college', 'I am a current or former College Mock Trial Competitor'),
    ('ls', 'I am a current or former Law School Mock Trial Competitor'),
    ('judged', 'I have judged 1-2 Mock Trial Competitions in the past'),
    ('judged_some', 'I have judged 3-5 Mock Trial Competitions in the past'),
    ('judged_many', 'I have judged 5 or more Mock Trial Competitions in the past'),
]


judged_rounds_choices = [
]

class Paradigm(models.Model):
    judge = models.OneToOneField('tourney.Judge', on_delete=models.CASCADE,
                                primary_key=True, related_name='paradigm')
    experience_years = models.DecimalField(default=0, max_digits=3, decimal_places=1, help_text='How many years of mock trial experience do you have?')
    experience_description = ArrayField(
        models.CharField(max_length=40, choices=experience_description_choices, null=True,
                         help_text='Do you have any experience competing or judging in high school, collegiate or law school mock trial competitions?',
                        blank=True),
        size=6, null=True, blank=True
    )
    affiliations = models.CharField(max_length=2000, null=True, blank=True)
    #scale On a scale of 1-10, I prefer mock trial attorneys who…
    comments = models.TextField(max_length=5000, null=True, blank=True)

role_choices = [
    ('att', 'Attorney'),
    ('wit', 'Witness')
]
class ParadigmPreference(models.Model):
    tournament = models.ForeignKey('tourney.Tournament', on_delete=models.SET_NULL, related_name='paradigm_preferences',
                                   related_query_name='paradigm_preference', null=True)
    role = models.CharField(max_length=40, choices=role_choices)
    low_end = models.CharField(max_length=40, null=True, blank=True)
    high_end = models.CharField(max_length=40, null=True, blank=True)

    def __str__(self):
        return f"{self.role.upper()}: {self.low_end} v. {self.high_end}"

class ParadigmPreferenceItem(models.Model):
    paradigm = models.ForeignKey(Paradigm, on_delete=models.CASCADE, related_name='preferences',
                                 related_query_name='preference_scale')
    paradigm_preference = models.ForeignKey(ParadigmPreference, on_delete=models.CASCADE, related_name='paradigm_preference_items',
                                   related_query_name='paradigm_preference_items', null=True)
    scale = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)],default=5)



