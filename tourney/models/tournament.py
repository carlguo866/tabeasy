from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

p_choices = [
    ('Prosecution','Criminal'),
    ('Plaintiff','Civil')
]


class Tournament(models.Model):
    name = models.CharField(max_length=40, help_text='Tournament Name:')
    wit_nums = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)],default=3,
                                   help_text='How many witnesses does each side call?')
    rank_nums = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=5,
                                    help_text='How many competitors (attorneys/witnesses) do judges rank?')
    p_choice = models.CharField(max_length=40, choices=p_choices,
                                help_text='Is your case a Civil or Criminal case')
    publish_ballot_scores = models.BooleanField(default=False,
                                                help_text='Do you want to publish ballot scores or just comments?')
    split_division = models.BooleanField(default=False)
    division_team_num = models.IntegerField(default=10,
                                            help_text='How many teams do you have?')
    individual_award_rank_plus_record = models.BooleanField(default=False,
                                                            help_text='Do you include the team\'s record when calculating individual awards?')
    case = models.URLField(max_length=200, null=True, blank=True,
                           help_text='Case Link:')
    roe = models.URLField(max_length=200, null=True, blank=True,
                          help_text='Rules of Evidence Link:')
    zoom_link = models.URLField(max_length=200, null=True, blank=True,
                                help_text='Zoom Meeting Link (leave blank if not applicable):')
    presiding_judge_script = models.URLField(max_length=200, null=True, blank=True,
                                             help_text='Presiding Judge Script (leave blank if not applicable):')
    hide_comments = models.BooleanField(default=False,
                                        help_text='Is the tournament in-person?')
    judges = models.IntegerField(default=2,
                                 help_text='How many judges do you count into the result?')
    conflict_other_side = models.BooleanField(default=True)
    hide_captains_meeting = models.BooleanField(default=False, help_text='Hide the captains meeting?')
    spirit = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name



