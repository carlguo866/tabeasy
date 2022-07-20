from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Team(AbstractUser):
    raw_password = models.CharField(
        max_length=128,
        default='THIS_IS_NOT_RECORDED',
        help_text='A read-only field to record password only for development.'
    )
    team_name = models.CharField(
        max_length=100,
        default='PPMT Team'
    )
    school = models.CharField(
        max_length=100,
        default = 'placeholder'
    )

    # team_members = ArrayField(
    #     models.CharField(max_length=100),
    #     size=10,
    # )

