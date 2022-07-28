import string
import random
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.forms import MultipleChoiceField
from django.forms.models import ModelChoiceIterator, BaseInlineFormSet

from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round, CaptainsMeeting
from tourney.models.team import Team, TeamMember

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
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
        fields = '__all__'
        exclude = ['pairing','extra_judge','courtroom']
        # widgets = {'courtroom': forms.HiddenInput()}

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

        if cleaned_data.get('p_team') == cleaned_data.get('d_team'):
            errors.append('one team cant compete against itself')
        if cleaned_data.get('p_team').next_side(self.instance.pairing.round_num) == 'd':
            errors.append(f"{cleaned_data.get('p_team')} is supposed to play d this round")
        if cleaned_data.get('d_team').next_side(self.instance.pairing.round_num) == 'p':
            errors.append(f"{cleaned_data.get('d_team')} is supposed to play p this round")
        if cleaned_data.get('presiding_judge') == cleaned_data.get('scoring_judge'):
            errors.append('assigning one judge for two roles')

        judges = [cleaned_data.get('presiding_judge'),cleaned_data.get('scoring_judge')]
        for judge in judges:
            if judge != None:
                #check conflict
                teams = [cleaned_data.get('p_team'), cleaned_data.get('d_team')]
                for team in teams:
                    if team in judge.conflicts.all():
                        errors.append(f"{judge} conflicted with p_team {team}")

                #check if judged
                judged = None
                for round in judge.rounds:
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

                # #check if assigned in another division
                pairings = Pairing.objects.filter(round_num=self.instance.pairing.round_num)
                if pairings.exists ():
                    for pairing in pairings.all():
                        if pairing != self.instance.pairing:
                            for round in pairing.rounds.all():
                                if judge in [round.presiding_judge,round.scoring_judge]:
                                    errors.append(f"{judge} already assigned in {pairing.division}")

        if errors != []:
            raise ValidationError(errors)
    # #
    # def save(self, commit=True):
    #     super().save()

class PairingFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        existing_judges = []
        existing_teams = []
        # existing_courtrooms = []
        errors = []

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            if form.cleaned_data == {}:
                continue
            form_judges = [form.cleaned_data.get('presiding_judge'),form.cleaned_data.get('scoring_judge')]
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
        fields = '__all__'
        exclude = ['round','judge']
        widgets = {
            'submit': forms.Select(choices=BOOL_CHOICES)
        }


    def __init__(self, *args, **kwargs):
        super(BallotForm, self).__init__(*args, **kwargs)
        if not self.instance.submit:
            for field in self.fields:
                self.fields[field].required = False

        if self.instance.round.captains_meeting.submit == True:
            att_list = TeamMember.objects.filter(pk__in=[att.pk for att in self.instance.round.captains_meeting.atts])
            self.fields['att_rank_1'].queryset = att_list
            self.fields['att_rank_2'].queryset = att_list
            self.fields['att_rank_3'].queryset = att_list
            self.fields['att_rank_4'].queryset = att_list
            wit_list = TeamMember.objects.filter(pk__in=[wit.pk for wit in self.instance.round.captains_meeting.wits])
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

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        if cleaned_data.get('submit'):
            for k,v in cleaned_data.items():
                if k.find('comment') == -1 and v == None:
                    errors.append(f"{k} empty")
        raise ValidationError(errors)

class CaptainsMeetingForm(forms.ModelForm):

    class Meta:
        model = CaptainsMeeting
        fields = '__all__'
        exclude = ['round']
        widgets = {
            'submit': forms.Select(choices=BOOL_CHOICES)
        }

    def __init__(self, *args, **kwargs):
        super(CaptainsMeetingForm, self).__init__(*args, **kwargs)
        if not self.instance.submit:
            for field in self.fields:
                self.fields[field].required = False

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

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        if cleaned_data.get('submit') == True:
            for k,v in cleaned_data.items():
                if v == None:
                    errors.append(f"{k} empty")

        if errors != []:
            raise ValidationError(errors)






