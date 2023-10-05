from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

p_choices = [
    ('Prosecution', 'Criminal'),
    ('Plaintiff', 'Civil')
]

# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return "tournament_{0}/{1}".format(instance.id, filename)


class Tournament(models.Model):
    name = models.CharField(max_length=40, help_text='Tournament Name:')
    short_name = models.CharField(max_length=10, help_text='Shortened Tournament Name:',
                                  validators=[RegexValidator(r'^[a-zA-Z0-9_-]+$', 'You can only enter alphanumerics, underscores, and dashes.')])
    wit_nums = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)], default=3,
                                   help_text='How many witnesses does each side call?')
    rank_nums = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=5,
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
                                        help_text='Do you want to hide comments on ballots?')
    judges = models.IntegerField(default=2,
                                 help_text='How many judges do you count into the result?')
    conflict_other_side = models.BooleanField(default=True)
    hide_captains_meeting = models.BooleanField(
        default=False, help_text='Hide the captains meeting?')
    spirit = models.BooleanField(
        default=False, help_text='Do you want to enable the spirit award functionality?')

    def __str__(self):
        return self.name
