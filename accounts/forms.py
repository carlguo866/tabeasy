from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import User, Team, Judge, Tab


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','is_team','is_judge', 'is_tab')

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = []


class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = []

class TabForm(forms.ModelForm):
    class Meta:
        model = Tab
        fields = []

