import string

from django import forms
from django.core.exceptions import ValidationError
from django.forms import MultipleChoiceField
from django.forms.models import ModelChoiceIterator, BaseInlineFormSet

from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round
from tourney.models.team import Team


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = []

class JudgeForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = []

class PairingForm(forms.ModelForm):
    class Meta:
        model = Pairing
        fields = ('round_num', 'division')


class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = ('courtroom','p_team','d_team','judges')
        # widgets = {
        #     'p_team': forms.Select(attrs={'size': 5}),
        #     'd_team': forms.Select(attrs={'size': 5}),
        #     'judge_1': forms.Select(attrs={'size': 5}),
        #     'judge_2': forms.Select(attrs={'size': 5})
        # }

    def __init__(self, pairing, *args, **kwargs):
        super(RoundForm, self).__init__(*args, **kwargs)
        self.fields['p_team'].queryset = Team.objects.filter(division=pairing.division)
        self.fields['d_team'].queryset = Team.objects.filter(division=pairing.division)

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        if cleaned_data.get('courtroom') not in string.ascii_uppercase:
            errors.append('Courtroom is not in the alphabet')
        if cleaned_data.get('judges').count() > 3:
            errors.append('more than 3 judges for a round')
        if cleaned_data.get('judges').count() < 2:
            errors.append('less than 2 judges for a round')
        if cleaned_data.get('p_team') == cleaned_data.get('d_team'):
            errors.appenderrors.append('one team cant compete against itself')
        for judge in cleaned_data.get('judges').all():
            if cleaned_data.get('p_team') in judge.conflicts.all():
                errors.append(f"{judge} conflicted with p_team {cleaned_data.get('p_team')}")
            if cleaned_data.get('d_team') in judge.conflicts.all():
                errors.append(f"{judge} conflicted with d_team {cleaned_data.get('d_team')}")
        if errors != []:
            raise ValidationError(errors)

class PairingFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        existing_judges = []
        existing_teams = []
        existing_courtrooms = []
        errors = []
        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if form.cleaned_data == {}:
                continue
            if form.cleaned_data.get('courtroom') in existing_courtrooms:
                errors.append(f"courtroom {form.cleaned_data.get('courtroom')} already in use")
            existing_courtrooms.append(form.cleaned_data.get('courtroom'))
            form_judges = form.cleaned_data.get('judges').all()
            for judge in form_judges:
                if judge in existing_judges:
                    errors.append(f'{judge} used twice!')
                existing_judges.append(judge)
            teams = [form.cleaned_data.get('p_team'),form.cleaned_data.get('d_team')]
            for team in teams:
                if team in existing_teams:
                    errors.append(f'{team} used twice!')
                existing_teams.append(team)
        if errors != []:
            raise ValidationError(errors)




class CustomModelChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj),
                self.field.label_from_instance(obj), obj)

class CustomModelChoiceField(forms.ModelMultipleChoiceField):
    def _get_choices(self):
        if hasattr(self, '_choices'):
            return self._choices
        return CustomModelChoiceIterator(self)
    choices = property(_get_choices,
                       MultipleChoiceField._set_choices)

class UpdateConflictForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ['conflicts']
    #
    # user = forms.Select()
    # conflicts_queryset = ( (team, team.school) for team in Team.objects.all() )
    conflicts = CustomModelChoiceField(
        # queryset=conflicts_queryset,
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class UpdateJudgeFriendForm(forms.ModelForm):
    class Meta:
        model = Judge
        fields = ['judge_friends']

    #
    # user = forms.Select()

    judge_friends = forms.ModelMultipleChoiceField(
        queryset=Judge.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class BallotForm(forms.ModelForm):
    class Meta:
        model = Ballot
        labels =  {'p_open': 'P Opening', 'p_open_comment': 'Comment', 'd_open': 'D Opening','d_open_comment': 'Comment'}
        fields = ['p_open','p_open_comment','d_open','d_open_comment',
              'p_wit1_wit_direct', 'p_wit1_att_direct', 'p_wit1_wit_cross','p_wit1_att_cross',
              'p_wit1_wit_direct_comment','p_wit1_wit_cross_comment','p_wit1_att_direct_comment','p_wit1_att_cross_comment',
              'p_wit2_wit_direct', 'p_wit2_att_direct', 'p_wit2_wit_cross', 'p_wit2_att_cross',
              'p_wit2_wit_cross_comment', 'p_wit2_att_direct_comment', 'p_wit2_att_cross_comment', 'p_wit2_wit_direct_comment',
              'p_wit3_wit_direct', 'p_wit3_att_direct', 'p_wit3_wit_cross', 'p_wit3_att_cross',
              'p_wit3_wit_cross_comment', 'p_wit3_att_direct_comment', 'p_wit3_att_cross_comment', 'p_wit3_wit_direct_comment',

              'd_wit1_wit_direct', 'd_wit1_att_direct', 'd_wit1_wit_cross', 'd_wit1_att_cross',
              'd_wit1_wit_direct_comment', 'd_wit1_wit_cross_comment', 'd_wit1_att_direct_comment',
              'd_wit1_att_cross_comment',
              'd_wit2_wit_direct', 'd_wit2_att_direct', 'd_wit2_wit_cross', 'd_wit2_att_cross',
              'd_wit2_wit_cross_comment', 'd_wit2_att_direct_comment', 'd_wit2_att_cross_comment',
              'd_wit2_wit_direct_comment',
              'd_wit3_wit_direct', 'd_wit3_att_direct', 'd_wit3_wit_cross', 'd_wit3_att_cross',
              'd_wit3_wit_cross_comment', 'd_wit3_att_direct_comment', 'd_wit3_att_cross_comment',
              'd_wit3_wit_direct_comment',
              'p_close','p_close_comment','d_close','d_close_comment',

              ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # self.fields['round'].queryset = self.request.user.judge.rounds.all()


