from django.core.exceptions import ValidationError
from django import forms

from submission.models.ballot import Ballot
from submission.models.captains_meeting import CaptainsMeeting, CharacterPronouns
from submission.models.section import BallotSection, CaptainsMeetingSection
from tourney.models import Competitor


INT_CHOICES = [(i , i) for i in range(11)]
class BallotForm(forms.ModelForm):
    class Meta:
        model = Ballot
        fields = '__all__'
        exclude = ['round','judge']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BallotForm, self).__init__(*args, **kwargs)

        if self.instance.round.pairing.round_num == 5 or not self.instance.submit:
            for field in self.fields:
                self.fields[field].required = False

        if self.instance.submit:
            for field in self.fields:
                self.fields[field].disabled = True

        if self.request.user.is_team:
            for field in self.fields:
                self.fields[field].disabled = True

        if self.request.user.is_judge and self.request.user.judge != self.instance.judge:
            for field in self.fields:
                self.fields[field].disabled = True

        if self.request.user.is_staff:
            self.fields['submit'].disabled = False

        if self.instance.round.captains_meeting.submit == True:
            att_list = Competitor.objects.filter(pk__in=[att.pk for att in self.instance.round.captains_meeting.atts])
            self.fields['att_rank_1'].queryset = att_list
            self.fields['att_rank_2'].queryset = att_list
            self.fields['att_rank_3'].queryset = att_list
            self.fields['att_rank_4'].queryset = att_list
            wit_list = Competitor.objects.filter(pk__in=[wit.pk for wit in self.instance.round.captains_meeting.wits])
            self.fields['wit_rank_1'].queryset = wit_list
            self.fields['wit_rank_2'].queryset = wit_list
            self.fields['wit_rank_3'].queryset = wit_list
            self.fields['wit_rank_4'].queryset = wit_list
        else:
            team_ids = [person.pk for person in Competitor.objects.filter(team=self.instance.round.p_team)] +\
                [person.pk for person in Competitor.objects.filter(team=self.instance.round.d_team)]
            individual_award_query = Competitor.objects.filter(pk__in=team_ids)
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
        if self.instance.round.pairing.round_num != 5 and cleaned_data.get('submit'):
            for k,v in cleaned_data.items():
                if k.find('comment') == -1 and v == None:
                    if k.find('att') != -1:
                        error = k.replace('att', 'Attorney').replace('rank','Rank')
                    else:
                        error = k.replace('wit', 'Witness').replace('rank','Rank')
                    error = ' '.join(error.split('_'))
                    errors.append(f"You have not assigned a competitor for {error}")

        if errors != []:
            raise ValidationError(errors)

class BallotSectionForm(forms.ModelForm):
    class Meta:
        model = BallotSection
        fields = ['score','comment']
        widgets = {
            'score': forms.Select(choices=INT_CHOICES),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.init_ballot = kwargs.pop('ballot', None)
        self.init_subsection = kwargs.pop('subsection', None)
        super(BallotSectionForm, self).__init__(*args, **kwargs)
        if self.init_ballot:
            self.instance.ballot = self.init_ballot
        if self.init_subsection:
            self.instance.subsection = self.init_subsection
        if self.instance.ballot.submit:
            for field in self.fields:
                self.fields[field].disabled = True

        if self.request.user.is_team:
            for field in self.fields:
                self.fields[field].disabled = True

        if self.request.user.is_judge and self.request.user.judge != self.instance.ballot.judge:
            for field in self.fields:
                self.fields[field].disabled = True

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
        if self.request.user.is_judge and not self.request.user.is_staff:
            for field in self.fields:
                self.fields[field].disabled = True

        if not self.instance.submit:
            for field in self.fields:
                self.fields[field].required = False


    #     p_team_members = Competitor.objects.filter(team=self.instance.round.p_team)
    #     self.fields['p_opener'].queryset = p_team_members
    #     self.fields['p_wit1'].queryset = p_team_members
    #     self.fields['p_wit1_direct_att'].queryset = p_team_members
    #     self.fields['p_wit2'].queryset = p_team_members
    #     self.fields['p_wit2_direct_att'].queryset = p_team_members
    #     self.fields['p_wit3'].queryset = p_team_members
    #     self.fields['p_wit3_direct_att'].queryset = p_team_members
    #     self.fields['d_wit1_cross_att'].queryset = p_team_members
    #     self.fields['d_wit2_cross_att'].queryset = p_team_members
    #     self.fields['d_wit3_cross_att'].queryset = p_team_members
    #     self.fields['p_closer'].queryset = p_team_members
    #
    #     d_team_members = Competitor.objects.filter(team=self.instance.round.d_team)
    #     self.fields['d_opener'].queryset = d_team_members
    #     self.fields['d_wit1'].queryset = d_team_members
    #     self.fields['d_wit1_direct_att'].queryset = d_team_members
    #     self.fields['d_wit2'].queryset = d_team_members
    #     self.fields['d_wit2_direct_att'].queryset = d_team_members
    #     self.fields['d_wit3'].queryset = d_team_members
    #     self.fields['d_wit3_direct_att'].queryset = d_team_members
    #     self.fields['p_wit1_cross_att'].queryset = d_team_members
    #     self.fields['p_wit2_cross_att'].queryset = d_team_members
    #     self.fields['p_wit3_cross_att'].queryset = d_team_members
    #     self.fields['d_closer'].queryset = d_team_members
    #
    # def clean(self):
    #     cleaned_data = super().clean()
    #     errors = []
    #     #after submission all fields need to be filled
    #     # if cleaned_data.get('submit') == True:
    #     #     for k,v in cleaned_data.items():
    #     #         if v == None:
    #     #             errors.append(f"{k} empty")
    #
    #     if errors != []:
    #         raise ValidationError(errors)

class CaptainsMeetingSectionForm(forms.ModelForm):
    class Meta:
        model = CaptainsMeetingSection
        fields = ['competitor','character']

    def __init__(self, *args, **kwargs):
        self.init_captains_meeting = kwargs.pop('captains_meeting', None)
        self.init_subsection = kwargs.pop('subsection', None)
        super(CaptainsMeetingSectionForm, self).__init__(*args, **kwargs)
        if self.init_captains_meeting:
            self.instance.captains_meeting = self.init_captains_meeting
        if self.init_subsection:
            self.instance.subsection = self.init_subsection

        p_team_members = Competitor.objects.filter(team=self.init_captains_meeting.round.p_team)
        d_team_members = Competitor.objects.filter(team=self.init_captains_meeting.round.d_team)
        if self.init_subsection.side == 'p':
            self.fields['competitor'].queryset = p_team_members
        else:
            self.fields['competitor'].queryset = d_team_members

        if not self.init_captains_meeting.submit:
            for field in self.fields:
                self.fields[field].required = False


