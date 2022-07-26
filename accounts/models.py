from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
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
        return f"{self.username}"

class Tab(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True, related_name='tab')
    available_rounds = models.IntegerField(default=1,validators=[MinValueValidator(1), MaxValueValidator(5)])


    def __str__(self):
        return f"Tab: {self.user.username}"