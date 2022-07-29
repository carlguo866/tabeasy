from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from accounts.models import User, Tab
from tabeasy_secrets.secret import JUDGE_VALIDATION_CODE


class SignUpForm(UserCreationForm):
    validation_code = forms.CharField(max_length=40)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')


    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('validation_code') != JUDGE_VALIDATION_CODE:
            raise ValidationError(
                        f"Wrong validation code, or ... you are not a judge?")


class TabForm(forms.ModelForm):
    class Meta:
        model = Tab
        fields = []

