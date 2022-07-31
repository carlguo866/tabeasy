from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import User
from tabeasy_secrets.secret import JUDGE_VERIFICATION_CODE
from django.utils.translation import gettext_lazy as _

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text="Must contain at least 4 characters.",
    )

    verification_code = forms.CharField(max_length=40, help_text='We sent this code by email in the instruction to verify that you are a judge.')


    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
        help_texts = {
            'username': 'Used for login and as a unique identifier of your '
                        'account. You won’t be able to change it later, '
                        'so choose wisely!',
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['verification_code'].label = 'Verification Code'

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('verification_code') != JUDGE_VERIFICATION_CODE:
            raise ValidationError(
                        f"Wrong validation code, or ... you are not a judge?")

