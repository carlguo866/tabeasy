from django import forms
from django.core.exceptions import ValidationError
from django.forms import MultipleChoiceField
from django.forms.models import ModelChoiceIterator, BaseInlineFormSet

from tabeasy.settings import DEBUG
from tourney.models.captains_meeting import CharacterPronouns
from tourney.models.judge import Judge
from tourney.models.round import Pairing, Round, CaptainsMeeting
from tourney.models.team import Team
from tourney.models.competitor import Competitor

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



class PairingSubmitForm(forms.ModelForm):
    class Meta:
        model = Pairing
        fields = ['team_submit', 'final_submit', 'publish']

class RoundForm(forms.ModelForm):
    class Meta:
        model = Round
        fields = '__all__'
        exclude = ['pairing','courtroom']
        # widgets = {
        #     'p_team': SearchableSelect(model='Round', search_field='p_team', limit=10),
        #     'd_team': SearchableSelect(model='Round', search_field='d_team', limit=10)
        # }
    # p_team = ajax_select_fields.AutoCompleteSelectField('p_team')


    def __init__(self, pairing, other_formset, *args, **kwargs):
        super(RoundForm, self).__init__(*args, **kwargs)
        self.other_formset = other_formset
        if pairing == None:
            self.fields['p_team'].queryset = Team.objects.all()
            self.fields['d_team'].queryset = Team.objects.all()
            self.fields['presiding_judge'].queryset = Judge.objects.filter(preside__gt=0)
        else:
            if not pairing.final_submit:
                for field in self.fields:
                    self.fields[field].required = False
            self.fields['p_team'].queryset = Team.objects.filter(division=pairing.division)
            self.fields['d_team'].queryset = Team.objects.filter(division=pairing.division)
            available_judges_pk = [judge.pk for judge in Judge.objects.all()
                                   if judge.get_availability(pairing.round_num)]
            self.fields['presiding_judge'].queryset = \
                Judge.objects.filter(pk__in=available_judges_pk, preside__gt=0,
                                     checkin=True).order_by('checkin','user__username')
            self.fields['scoring_judge'].queryset = Judge.objects.filter(pk__in=available_judges_pk,
                                                                         checkin=True).order_by('checkin','user__username')
            self.fields['extra_judge'].queryset = Judge.objects.filter(pk__in=available_judges_pk,
                                                                         checkin=True).order_by('checkin',
                                                                                                'user__username')

    def clean(self):
        cleaned_data = super().clean()
        errors = []

        #check for judges
        if self.other_formset != None and self.instance.pairing.final_submit:
            form_judges = [cleaned_data.get('presiding_judge'), cleaned_data.get('scoring_judge'),
                           cleaned_data.get('extra_judge')]
            for form in self.other_formset:
                if form.cleaned_data == {} and not DEBUG:
                    raise ValidationError('You don\'t have enough rounds.')
                elif form.cleaned_data == {} and DEBUG:
                    continue

                other_form_judges = [form.cleaned_data.get('presiding_judge'),
                                     form.cleaned_data.get('scoring_judge'), form.cleaned_data.get('extra_judge')]
                # #check if assigned in another division this should be done on the form level
                for judge in form_judges:
                    if judge and judge in other_form_judges:
                        errors.append(f"{other_form_judges} {form_judges} {judge} already assigned in {form.instance.pairing.division}")

        if errors != []:
            raise ValidationError(errors)


    def save(self, commit=True):
        would_save = False
        for k, v in self.instance.__dict__.items():
            if k in ['p_team_id','d_team_id','presiding_judge_id','scoring_judge_id'] and v != None:
                would_save = True
        if would_save:
            super().save()



class PairingFormSet(BaseInlineFormSet):

    # def __init__(self, *args, **kwargs):
    #     self.other_form = kwargs.pop('other_form')
    #     super(PairingFormSet, self).__init__(*args, **kwargs)


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
                if form.cleaned_data == {} and not DEBUG:
                    raise ValidationError('You don\'t have enough rounds.')
                elif form.cleaned_data == {} and DEBUG:
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
                form_judges = [form.cleaned_data.get('presiding_judge'),
                               form.cleaned_data.get('scoring_judge'), form.cleaned_data.get('extra_judge')]
                for judge in form_judges:
                    if judge:
                        if judge in existing_judges:
                            errors.append(f'{judge} used twice!')
                        existing_judges.append(judge)

        if errors != []:
            raise ValidationError(errors)


class CustomModelChoiceIterator(ModelChoiceIterator):
    def choice(self, obj):
        return (self.field.prepare_value(obj),
                self.field.label_from_instance(obj), obj)
        # return obj

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


class CheckinJudgeForm(forms.Form):

    checkins = forms.ModelMultipleChoiceField(
        queryset=Judge.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        round_num = kwargs.pop('round_num')
        super(CheckinJudgeForm, self).__init__(*args, **kwargs)
        available_judges_pk = [judge.pk for judge in Judge.objects.all()
                               if judge.get_availability(round_num)]
        self.fields['checkins'].queryset = Judge.objects.filter(checkin=False, pk__in=available_judges_pk)


class EditPronounsForm(forms.ModelForm):
    class Meta:
        model = CharacterPronouns
        fields = ['pronouns']

    def __init__(self, *args, **kwargs):
        self.init_character = kwargs.pop('character', None)
        self.init_captains_meeting = kwargs.pop('captains_meeting', None)
        super(EditPronounsForm, self).__init__(*args, **kwargs)
        if self.init_character:
            self.instance.character = self.init_character
        if self.init_captains_meeting:
            self.instance.captains_meeting = self.init_captains_meeting



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


        p_team_members = Competitor.objects.filter(team=self.instance.round.p_team)
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

        d_team_members = Competitor.objects.filter(team=self.instance.round.d_team)
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
        # if cleaned_data.get('submit') == True:
        #     for k,v in cleaned_data.items():
        #         if v == None:
        #             errors.append(f"{k} empty")

        if errors != []:
            raise ValidationError(errors)



