from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from tourney.models.team import Team
 
class Spirit(models.Model): 
    team = models.OneToOneField(Team, on_delete=models.CASCADE, primary_key=True,
                                related_name='spirit', default="")
    
    round1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    round2 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    round3 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    # round4 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    q1 = models.TextField(max_length=5000, null=True, blank=True, help_text="Please list any reasons that you think one of the teams you competed against is especially deserving of the Spirit Award. Please provide a specific example, if possible.")
    
    q2 = models.TextField(max_length=5000, null=True, blank=True, help_text="Please list any team that you didn’t compete against but that you believe exhibited mock trial's ideals and, therefore, should receive additional consideration for the Spirit Award. Please provide a specific example.")
    submit = models.BooleanField(default=False, help_text='Submit')

    def get_score(self, round_num): 
        assert round_num in [1,2,3]
        if round_num == 1: 
            return self.round1
        elif round_num == 2:
            return self.round2
        elif round_num == 3:
            return self.round3
        # elif round_num == 4:
        #     return self.round4

    def __str__(self):
        return f"{self.team.__str__()} Spirit Form" 
    
    def clean(self):
        errors = []

        if errors != []:
            raise ValidationError(errors)
