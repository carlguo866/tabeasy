from django import forms
from tourney.models.judge import Judge
from tourney.models.round import Pairing, PairingItem
from tourney.models.team import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = []

class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = []



GEEKS_CHOICES = (
    ("1", "One"),
    ("2", "Two"),
    ("3", "Three"),
    ("4", "Four"),
    ("5", "Five"),
)

class PairingFormSimple(forms.Form):
    geeks_field = forms.ChoiceField(choices=GEEKS_CHOICES)

# class PairingForm(forms.ModelForm):
#     class Meta:
#         model = Pairing
        # fields = ('round', 'div_1', 'div_2')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['div_2'].queryset = Team.objects.all()

class RoundForm(forms.ModelForm):
    class Meta:
        model = PairingItem
        fields = ('courtroom','p_team','d_team','judge_1','judge_2')
        # widgets = {
        #     'p_team': forms.Select(attrs={'size': 5}),
        #     'd_team': forms.Select(attrs={'size': 5}),
        #     'judge_1': forms.Select(attrs={'size': 5}),
        #     'judge_2': forms.Select(attrs={'size': 5})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['p_team'].queryset = Team.objects.all() #filter(division='Disney')
        # if 'pairing' in self.data:
        #     # try:
        #     division = int(self.data.get('pairing').get('division'))
        #     print(division)
        #     self.fields['p_team'].queryset = Team.objects.filter(country_id=division).order_by('team_name')
        #     # except (ValueError, TypeError):
        #     #     print('error ')
        #     #     pass
        # else:
        #     print('error hereeee')

        # self.fields['p_team'].queryset = Team.objects.filter(self.)
        self.fields['d_team'].queryset = Team.objects.all()
        self.fields['judge_1'].queryset = Judge.objects.all()
        self.fields['judge_2'].queryset = Judge.objects.all()

class UpdateConflictForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ['conflicts']
    #
    # user = forms.Select()

    conflicts = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )