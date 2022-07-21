from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django import forms
from django_better_admin_arrayfield.models.fields  import ArrayField

class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.TypedMultipleChoiceField,
            'choices': self.base_field.choices,
            'coerce': self.base_field.to_python,
            'widget': forms.CheckboxSelectMultiple,
        }
        defaults.update(kwargs)

        return super(ArrayField, self).formfield(**defaults)

class Team(AbstractUser):
    id = models.AutoField(primary_key=True)
    raw_password = models.CharField(
        max_length=128,
        default='THIS_IS_NOT_RECORDED',
        help_text='A read-only field to record password only for development.'
    )
    team_name = models.CharField(
        max_length=100,
        default='PPMT Team'
    )
    division = models.CharField(
        max_length=100,
        default='Division'
    )
    school = models.CharField(
        max_length=100,
        default = 'placeholder'
    )
    team_roster = ArrayField(
        base_field=models.CharField(max_length=100),
        size=10,
        null=True,
        blank=True
    )
    sides_choices = [('P','Prosecution'),('D','Defense')]
    sides = ArrayField(
        models.CharField(max_length=1, choices=sides_choices),
        size=4,
        null=True,
        blank=True
    )
    ballots = models.DecimalField(max_digits=3, decimal_places=1,null=True, blank=True)
    cs = models.DecimalField(max_digits=3, decimal_places=1,null=True, blank=True)
    pd = models.IntegerField(
        null=True, blank=True
    )


