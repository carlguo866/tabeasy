import string

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.forms import MultipleChoiceField
from django.forms.models import ModelChoiceIterator, BaseInlineFormSet

from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round, CaptainsMeeting
from tourney.models.team import Team, TeamMember


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
        if pairing == None:
            self.fields['p_team'].queryset = Team.objects.all()
            self.fields['d_team'].queryset = Team.objects.all()
        else:
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
            teams = [cleaned_data.get('p_team'), cleaned_data.get('d_team')]
            for team in teams:
                if team in judge.conflicts.all():
                    errors.append(f"{judge} conflicted with p_team {team}")
            judged = None
            for round in judge.rounds.all():
                if round != self.instance:
                    if judged == None:
                        judged = Team.objects.filter(pk=round.p_team.pk)
                    else:
                        judged |= Team.objects.filter(pk=round.p_team.pk)
                    judged |= Team.objects.filter(pk=round.d_team.pk)
            if judged != None:
                for team in teams:
                    if team in judged:
                        errors.append(f"{judge} has judged p_team {team}")
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
                  'att_rank_1', 'att_rank_2', 'att_rank_3', 'att_rank_4',
                  'wit_rank_1', 'wit_rank_2', 'wit_rank_3', 'wit_rank_4',
              ]

    def __init__(self, *args, **kwargs):
        super(BallotForm, self).__init__(*args, **kwargs)
        if self.instance.round.captains_meeting.submit == True:
            att_id = [self.instance.round.captains_meeting.p_wit1_direct_att.pk,
                      self.instance.round.captains_meeting.p_wit2_direct_att.pk,
                      self.instance.round.captains_meeting.p_wit3_direct_att.pk,
                      self.instance.round.captains_meeting.d_wit1_direct_att.pk,
                      self.instance.round.captains_meeting.d_wit2_direct_att.pk,
                      self.instance.round.captains_meeting.d_wit3_direct_att.pk,
                      ]
            att_list = TeamMember.objects.filter(pk__in=att_id)
            self.fields['att_rank_1'].queryset = att_list
            self.fields['att_rank_2'].queryset = att_list
            self.fields['att_rank_3'].queryset = att_list
            self.fields['att_rank_4'].queryset = att_list

            wit_id = [self.instance.round.captains_meeting.p_wit1.pk,
                      self.instance.round.captains_meeting.p_wit2.pk,
                      self.instance.round.captains_meeting.p_wit3.pk,
                      self.instance.round.captains_meeting.d_wit1.pk,
                      self.instance.round.captains_meeting.d_wit2.pk,
                      self.instance.round.captains_meeting.d_wit3.pk,
                      ]
            wit_list = TeamMember.objects.filter(pk__in=wit_id)
            self.fields['wit_rank_1'].queryset = wit_list
            self.fields['wit_rank_2'].queryset = wit_list
            self.fields['wit_rank_3'].queryset = wit_list
            self.fields['wit_rank_4'].queryset = wit_list
        else:
            individual_award_query = TeamMember.objects.filter(team=self.instance.round.p_team).union(
                                            TeamMember.objects.filter(team=self.instance.round.d_team))
            self.fields['att_rank_1'].queryset = individual_award_query
            self.fields['att_rank_2'].queryset = individual_award_query
            self.fields['att_rank_3'].queryset = individual_award_query
            self.fields['att_rank_4'].queryset = individual_award_query
            self.fields['wit_rank_1'].queryset = individual_award_query
            self.fields['wit_rank_2'].queryset = individual_award_query
            self.fields['wit_rank_3'].queryset = individual_award_query
            self.fields['wit_rank_4'].queryset = individual_award_query


class CaptainsMeetingForm(forms.ModelForm):
    class Meta:
        model = CaptainsMeeting
        fields = '__all__'
        exclude = ['round']

    def __init__(self, *args, **kwargs):
        super(CaptainsMeetingForm, self).__init__(*args, **kwargs)
        p_team_members = TeamMember.objects.filter(team=self.instance.round.p_team)
        self.fields['p_opener'].queryset = p_team_members
        self.fields['p_wit1'].queryset = p_team_members
        self.fields['p_wit1_direct_att'].queryset = p_team_members
        self.fields['p_wit2'].queryset = p_team_members
        self.fields['p_wit2_direct_att'].queryset = p_team_members
        self.fields['p_wit3'].queryset = p_team_members
        self.fields['p_wit3_direct_att'].queryset = p_team_members
        self.fields['d_wit1_cross_att'].queryset = p_team_members
        self.fields['d_wit2_cross_att'].queryset = p_team_members
        self.fields['d_wit3_cross_att'].queryset = p_team_members
        self.fields['p_closer'].queryset = p_team_members

        d_team_members = TeamMember.objects.filter(team=self.instance.round.d_team)
        self.fields['d_opener'].queryset = d_team_members
        self.fields['d_wit1'].queryset = d_team_members
        self.fields['d_wit1_direct_att'].queryset = d_team_members
        self.fields['d_wit2'].queryset = d_team_members
        self.fields['d_wit2_direct_att'].queryset = d_team_members
        self.fields['d_wit3'].queryset = d_team_members
        self.fields['d_wit3_direct_att'].queryset = d_team_members
        self.fields['p_wit1_cross_att'].queryset = d_team_members
        self.fields['p_wit2_cross_att'].queryset = d_team_members
        self.fields['p_wit3_cross_att'].queryset = d_team_members
        self.fields['d_closer'].queryset = d_team_members