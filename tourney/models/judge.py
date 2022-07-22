from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

from accounts.models import User
from tourney.models.team import Team

class Judge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='judge')
    # judged_round_1 =models.ForeignKey(Ballot, on_delete=models.CASCADE,
    #                             related_name='ballot1',blank=True, null=True)
    # judged_round_2 = models.ForeignKey(Ballot, on_delete=models.CASCADE,
    #                             related_name='ballot2', blank=True, null=True)
    # judged_round_3 = models.ForeignKey(Ballot, on_delete=models.CASCADE,
    #                             related_name='ballot3', blank=True, null=True)
    # judged_round_4 = models.ForeignKey(Ballot, on_delete=models.CASCADE,
    #                             related_name='ballot4', blank=True, null=True)

    conflicts = models.ManyToManyField(
        Team,
        blank=True
    )

    judge_friends = models.ManyToManyField(
        'self',
        blank=True
    )
    def __str__(self):
        return f"Judge: {self.user.username}"