from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

from tourney.models import Pairing


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    raw_password = models.CharField(
        max_length=128,
        default='THIS_IS_NOT_RECORDED',
        help_text='A read-only field to record password only for development.'
    )
    is_judge = models.BooleanField(default=True)
    is_team = models.BooleanField(default=False)
    tournament = models.ForeignKey('tourney.Tournament', on_delete=models.SET_NULL, related_name='users',
                                   related_query_name='user', null=True)

    def available_pairings(self):
        return [pairing for pairing in Pairing.objects.filter(tournament=self.tournament).order_by('round_num').all() if pairing.team_submit]

    def __str__(self):
        if self.is_team and getattr(self, "team", None):
            return self.team.team_name
        else:
            if self.first_name and self.last_name:
                return f"{self.first_name.title()} {self.last_name.title()}"
            elif self.first_name:
                return f"{self.first_name.title()}"
            else:
                return f"{self.username}"