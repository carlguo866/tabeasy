from django import forms
from django.forms import MultipleChoiceField
from django.forms.models import ModelChoiceIterator

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
        fields = ('courtroom','p_team','d_team','judge_1','judge_2')
        # widgets = {
        #     'p_team': forms.Select(attrs={'size': 5}),
        #     'd_team': forms.Select(attrs={'size': 5}),
        #     'judge_1': forms.Select(attrs={'size': 5}),
        #     'judge_2': forms.Select(attrs={'size': 5})
        # }

    def __init__(self, pairing, *args, **kwargs):
        super(RoundForm, self).__init__(*args, **kwargs)
        # self.fields['p_team'].queryset = Team.objects.all() #filter(division='Disney')
        # # if 'pairing' in self.data:
        # #     # try:
        # #     division = int(self.data.get('pairing').get('division'))
        # #     print(division)
        # #     self.fields['p_team'].queryset = Team.objects.filter(country_id=division).order_by('team_name')
        # #     # except (ValueError, TypeError):
        # #     #     print('error ')
        # #     #     pass
        # # else:
        # #     print('error hereeee')
        self.fields['p_team'].queryset = Team.objects.filter(division=pairing.division)
        self.fields['d_team'].queryset = Team.objects.filter(division=pairing.division)
        self.fields['judge_1'].queryset = Judge.objects.all()
        self.fields['judge_2'].queryset = Judge.objects.all()


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
              'p_close','p_close_comment','d_close','d_close_comment'
              ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # self.fields['round'].queryset = self.request.user.judge.rounds.all()


