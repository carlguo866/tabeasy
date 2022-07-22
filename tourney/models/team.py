from django.db import models
from django_better_admin_arrayfield.models.fields  import ArrayField

from accounts.models import User


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True, help_text="enter integer only")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team', null=True,blank=True)

    team_name = models.CharField(
        max_length=100,
        default='PPMT Team',
        null=True
    )
    division_choices = [('Disney', 'Disney'), ('Universal', 'Universal')]
    division = models.CharField(
        max_length=100,
        choices=division_choices,
        null=True
    )
    school = models.CharField(
        max_length=100,
        default='placeholder',
        null=True
    )
    team_roster = ArrayField(
        base_field=models.CharField(max_length=100),
        size=10,
        null=True,
        blank=True
    )
    side_choices = [('P', 'Prosecution'), ('D', 'Defense')]
    sides = ArrayField(
        models.CharField(max_length=1, choices=side_choices),
        size=4,
        null=True,
        blank=True
    )
    # ballots = ArrayField(
    #     models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True),
    #     size=4,
    #     null=True,
    #     blank=True
    # )
    cs = ArrayField(
        models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True),
        size=4,
        null=True,
        blank=True
    )
    pd = ArrayField(
        models.IntegerField(null=True, blank=True),
        size=4,
        null=True,
        blank=True
    )
    def __str__(self):
        return f"Team: {self.team_name}"

    def total_ballots(self):
        total = 0
        for each in self.ballots:
            if each is not None:
                total+= each
        return total

    def total_cs(self):
        total = 0
        for each in self.cs:
            if each is not None:
                total += each
        return total

    def total_pd(self):
        total = 0
        for each in self.pd:
            if each is not None:
                total += each
        return total

