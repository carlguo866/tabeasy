import string
import random
from django import forms
from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField
from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.forms import MultipleChoiceField
from django.forms.models import ModelChoiceIterator, BaseInlineFormSet

from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round, CaptainsMeeting
from tourney.models.team import Team, TeamMember

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))
INT_CHOICES = [(i,i) for i in range(11)]
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = []

JUDGE_AVAILABILITY_CHOICES = [
    ('available_round1', 'Round 1'),
    ('available_round2', 'Round 2'),
    ('available_round3', 'Round 3'),
    ('available_round4', 'Round 4'),
]
class JudgeForm(forms.ModelForm):

    availability = forms.MultipleChoiceField(
        choices=JUDGE_AVAILABILITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Judge
        fields = ['preside']

    def __init__(self, *args, **kwargs):
        super(JudgeForm, self).__init__(*args, **kwargs)
        self.fields['availability'].label = "Which round(s) would you like to judge?"
        initial_availability = []
        for round, _ in JUDGE_AVAILABILITY_CHOICES:
            if getattr(self.instance, round):
                initial_availability.append(round)
        self.fields['availability'].initial = initial_availability

    def save(self, commit=True):
        m = super(JudgeForm, self).save(commit=False)
        for round, _ in JUDGE_AVAILABILITY_CHOICES:
            if round in self.cleaned_data.get('availability'):
                setattr(m, round, True)
            else:
                setattr(m, round, False)
        if commit:
            m.save()
        return m



# class PairingForm(forms.ModelForm):
#     class Meta:
#         model = Pairing
#         fields = ('round_num', 'division','submit')

class PairingSubmitForm(forms.ModelForm):
    class Meta:
        model = Pairing
        fields = ['team_submit', 'final_submit']




class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = '__all__'
        exclude = ['pairing','courtroom','extra_judge']
        # widgets = {'courtroom': forms.HiddenInput()}

    def __init__(self, pairing, *args, **kwargs):
        super(RoundForm, self).__init__(*args, **kwargs)
        if pairing == None:
            self.fields['p_team'].queryset = Team.objects.all()
            self.fields['d_team'].queryset = Team.objects.all()
            self.fields['presiding_judge'].queryset = Judge.objects.filter(preside__gt=0)
        else:
            if not pairing.team_submit and not pairing.final_submit:
                for field in self.fields:
                    self.fields[field].required = False
            self.fields['p_team'].queryset = Team.objects.filter(division=pairing.division)
            self.fields['d_team'].queryset = Team.objects.filter(division=pairing.division)
            available_judges_pk = [judge.pk for judge in Judge.objects.all()
                                   if judge.get_availability(pairing.round_num)]
            self.fields['presiding_judge'].queryset = \
                Judge.objects.filter(pk__in=available_judges_pk, preside__gt=0).order_by('user__username')
            self.fields['scoring_judge'].queryset = Judge.objects.filter(pk__in=available_judges_pk).order_by('user__username')

    def save(self, commit=True):
        would_save = False
        for k, v in self.instance.__dict__.items():
            if k in ['p_team_id','d_team_id','presiding_judge_id','scoring_judge_id'] and v != None:
                would_save = True
        if would_save:
            super().save()



class PairingFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if any(self.errors):
            return
        existing_judges = []
        existing_teams = []
        errors = []
        if self.instance.team_submit or self.instance.final_submit:
            for form in self.forms:
                if self.can_delete and self._should_delete_form(form):
                    continue
                if form.cleaned_data == {}:
                    continue
                teams = [form.cleaned_data.get('p_team'),form.cleaned_data.get('d_team')]
                for team in teams:
                    if team in existing_teams:
                        errors.append(f'{team} used twice!')
                    existing_teams.append(team)

        if self.instance.final_submit:
            for form in self.forms:
                if self.can_delete and self._should_delete_form(form):
                    continue
                if form.cleaned_data == {}:
                    continue
                form_judges = [form.cleaned_data.get('presiding_judge'), form.cleaned_data.get('scoring_judge')]
                for judge in form_judges:
                    if judge in existing_judges:
                        errors.append(f'{judge} used twice!')
                    existing_judges.append(judge)

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
        labels =  {'p_open': 'Prosecution Opening',
                   'd_open': 'Defense Opening',
                   'p_close': 'Prosecution Closing',
                   'd_close': 'Defense Closing',
                   }
        fields = '__all__'
        exclude = ['round','judge']
        widgets = {
            'p_open': forms.Select(choices=INT_CHOICES),
            'd_open': forms.Select(choices=INT_CHOICES),
            'p_wit1_wit_direct': forms.Select(choices=INT_CHOICES),
            'p_wit1_wit_cross': forms.Select(choices=INT_CHOICES),
            'p_wit1_att_direct': forms.Select(choices=INT_CHOICES),
            'p_wit1_att_cross': forms.Select(choices=INT_CHOICES),
            'p_wit2_wit_direct': forms.Select(choices=INT_CHOICES),
            'p_wit2_wit_cross': forms.Select(choices=INT_CHOICES),
            'p_wit2_att_direct': forms.Select(choices=INT_CHOICES),
            'p_wit2_att_cross': forms.Select(choices=INT_CHOICES),
            'p_wit3_wit_direct': forms.Select(choices=INT_CHOICES),
            'p_wit3_wit_cross': forms.Select(choices=INT_CHOICES),
            'p_wit3_att_direct': forms.Select(choices=INT_CHOICES),
            'p_wit3_att_cross': forms.Select(choices=INT_CHOICES),
            'd_wit1_wit_direct': forms.Select(choices=INT_CHOICES),
            'd_wit1_wit_cross': forms.Select(choices=INT_CHOICES),
            'd_wit1_att_direct': forms.Select(choices=INT_CHOICES),
            'd_wit1_att_cross': forms.Select(choices=INT_CHOICES),
            'd_wit2_wit_direct': forms.Select(choices=INT_CHOICES),
            'd_wit2_wit_cross': forms.Select(choices=INT_CHOICES),
            'd_wit2_att_direct': forms.Select(choices=INT_CHOICES),
            'd_wit2_att_cross': forms.Select(choices=INT_CHOICES),
            'd_wit3_wit_direct': forms.Select(choices=INT_CHOICES),
            'd_wit3_wit_cross': forms.Select(choices=INT_CHOICES),
            'd_wit3_att_direct': forms.Select(choices=INT_CHOICES),
            'd_wit3_att_cross': forms.Select(choices=INT_CHOICES),
            'p_close': forms.Select(choices=INT_CHOICES),
            'd_close': forms.Select(choices=INT_CHOICES),
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
        if errors != []:
            raise ValidationError(errors)

class CaptainsMeetingForm(forms.ModelForm):

    class Meta:
        model = CaptainsMeeting
        fields = '__all__'
        exclude = ['round']
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(CaptainsMeetingForm, self).__init__(*args, **kwargs)
        if self.request.user.is_judge:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True

        if not self.instance.submit:
            for field in self.fields:
                self.fields[field].required = False
        for i, _ in enumerate(self.instance.character_evidence_options()):
            self.fields[f'character_evidence_option{i + 1}_description'].required = False


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
        #after submission all fields need to be filled
        if cleaned_data.get('submit') == True:
            for k,v in cleaned_data.items():
                if v == None:
                    errors.append(f"{k} empty")

        if errors != []:
            raise ValidationError(errors)




