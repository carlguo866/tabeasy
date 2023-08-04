from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from tourney.models.team import Team
 
class Spirit(models.Model): 
    team = models.OneToOneField(Team, on_delete=models.SET_NULL, primary_key=True,
                                related_name='spirit')
    
    round1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    round2 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    round3 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    round4 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    submit = models.BooleanField(default=False, help_text='Submit')

    def get_score(self, round_num): 
        assert round_num in [1,2,3,4]
        if round_num == 1: 
            return self.round1
        elif round_num == 2:
            return self.round2
        elif round_num == 3:
            return self.round3
        elif round_num == 4:
            return self.round4

    def __str__(self):
        return f"{self.team.__str__()} Spirit Form" 
    
    def clean(self):
        errors = []

        if errors != []:
            raise ValidationError(errors)