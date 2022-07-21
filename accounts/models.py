from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django import forms
from django_better_admin_arrayfield.models.fields  import ArrayField

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    raw_password = models.CharField(
        max_length=128,
        default='THIS_IS_NOT_RECORDED',
        help_text='A read-only field to record password only for development.'
    )
    is_judge = models.BooleanField(default=False)
    is_team = models.BooleanField(default=True)
    is_tab = models.BooleanField(default=False)
    def __str__(self):
        return f"User: {self.username}"

class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='team')
    # klass = models.ForeignKey('classroom.Class', on_delete=models.SET_NULL,
    #                           related_name='students',
    #                           related_query_name='student',
    #                           null=True, blank=True)

    team_name = models.CharField(
        max_length=100,
        default='PPMT Team',
        null=True
    )
    division_choices = [('div_1', 'Disney'), ('div_2', 'Universal')]
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
    ballots = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    cs = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    pd = models.IntegerField(
        null=True, blank=True
    )
    def __str__(self):
        return f"Team: {self.team_name}"

class Judge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='judge')
    # judged_rounds = ArrayField(
    #
    # )
    def __str__(self):
        return f"Judge: {self.user.username}"

class Tab(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='tab')

    def __str__(self):
        return f"Tab: {self.user.username}"