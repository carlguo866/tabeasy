from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

from accounts.models import User
from tourney.models.team import Team

class Judge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='judge')
    conflicts = models.ManyToManyField(
        Team,
        null=True,
        blank=True
    )

    judge_friends = models.ManyToManyField(
        'self',
        null=True,
        blank=True
    )
    def __str__(self):
        if self.user.first_name != None and self.user.first_name != '':
            return f"{self.user.first_name[0].upper()+self.user.first_name[1:]} {self.user.last_name[0].upper()+self.user.last_name[1:]}"
        else:
            return f"{self.user.username}"