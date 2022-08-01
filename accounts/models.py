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
    is_tab = models.BooleanField(default=False)


    def available_pairings(self):
        if not self.is_staff:
            return None
        else:
            return [pairing for pairing in Pairing.objects.order_by('round_num').all() if pairing.final_submit]

    def __str__(self):
        if self.is_team:
            return f"{self.team.team_name}"
        else:
            if self.first_name != None and self.first_name != '':
                return f"{self.first_name[0].upper() + self.first_name[1:]} {self.last_name[0].upper() + self.last_name[1:]}"
            else:
                return f"{self.username}"