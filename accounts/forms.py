from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import Team

class SignUpForm(UserCreationForm):

    class Meta:
        model = Team
        fields = ('username', 'password1', 'password2')