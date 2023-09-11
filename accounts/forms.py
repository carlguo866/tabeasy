from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import User
from tabeasy_secrets.secret import JUDGE_VERIFICATION_CODE
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Must contain at least 4 characters.",
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2','tournament')
        help_texts = {
            'username': 'Used for login and as a unique identifier of your '
                        'account. You won’t be able to change it later, '
                        'so choose wisely!',
        }

    def __init__(self, *args, **kwargs):
        team_signup = kwargs.pop('team_signup', None)
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        validator = RegexValidator(r'^[a-zA-Z0-9_-]+$',
                               'You can only enter alphanumerics, underscores, and dashes.')
        self.fields['username'].validators = [validator]
        if team_signup:
            del self.fields['first_name']
            del self.fields['last_name']



class UserTournamentForm(forms.ModelForm): 
    class Meta:
        model = User
        fields = ['tournament']
        exclude = ['split_division', 'rank_nums', 'conflict_other_side']
    

