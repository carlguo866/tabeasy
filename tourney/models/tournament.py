from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

p_choices = [
    ('Prosecution','Prosecution'),
    ('Plaintiff','Plaintiff')
]
class Tournament(models.Model):
    name = models.CharField(max_length=40)
    section_nums = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)],default=3)
    rank_nums = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=5)
    p_choice = models.CharField(max_length=40, choices=p_choices)
    publish_ballot_scores = models.BooleanField(default=False)
    split_division = models.BooleanField(default=False)
    division_team_num = models.IntegerField(default=10)

    def __str__(self):
        return self.name



