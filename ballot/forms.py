from django.core.exceptions import ValidationError
from django import forms

from ballot.models import Ballot
from ballot.models.section import BallotSection
from tourney.models import TeamMember


INT_CHOICES = [(i,i) for i in range(11)]
class BallotForm(forms.ModelForm):
    class Meta:
        model = Ballot
        # labels =  {'p_open': 'Prosecution Opening',
        #            'd_open': 'Defense Opening',
        #            'p_close': 'Prosecution Closing',
        #            'd_close': 'Defense Closing',
        #            }
        fields = '__all__'
        exclude = ['round','judge']
        # widgets = {
        #     'p_open': forms.Select(choices=INT_CHOICES),
        #     'd_open': forms.Select(choices=INT_CHOICES),
        #     'p_wit1_wit_direct': forms.Select(choices=INT_CHOICES),
        #     'p_wit1_wit_cross': forms.Select(choices=INT_CHOICES),
        #     'p_wit1_att_direct': forms.Select(choices=INT_CHOICES),
        #     'p_wit1_att_cross': forms.Select(choices=INT_CHOICES),
        #     'p_wit2_wit_direct': forms.Select(choices=INT_CHOICES),
        #     'p_wit2_wit_cross': forms.Select(choices=INT_CHOICES),
        #     'p_wit2_att_direct': forms.Select(choices=INT_CHOICES),
        #     'p_wit2_att_cross': forms.Select(choices=INT_CHOICES),
        #     'p_wit3_wit_direct': forms.Select(choices=INT_CHOICES),
        #     'p_wit3_wit_cross': forms.Select(choices=INT_CHOICES),
        #     'p_wit3_att_direct': forms.Select(choices=INT_CHOICES),
        #     'p_wit3_att_cross': forms.Select(choices=INT_CHOICES),
        #     'd_wit1_wit_direct': forms.Select(choices=INT_CHOICES),
        #     'd_wit1_wit_cross': forms.Select(choices=INT_CHOICES),
        #     'd_wit1_att_direct': forms.Select(choices=INT_CHOICES),
        #     'd_wit1_att_cross': forms.Select(choices=INT_CHOICES),
        #     'd_wit2_wit_direct': forms.Select(choices=INT_CHOICES),
        #     'd_wit2_wit_cross': forms.Select(choices=INT_CHOICES),
        #     'd_wit2_att_direct': forms.Select(choices=INT_CHOICES),
        #     'd_wit2_att_cross': forms.Select(choices=INT_CHOICES),
        #     'd_wit3_wit_direct': forms.Select(choices=INT_CHOICES),
        #     'd_wit3_wit_cross': forms.Select(choices=INT_CHOICES),
        #     'd_wit3_att_direct': forms.Select(choices=INT_CHOICES),
        #     'd_wit3_att_cross': forms.Select(choices=INT_CHOICES),
        #     'p_close': forms.Select(choices=INT_CHOICES),
        #     'd_close': forms.Select(choices=INT_CHOICES),
        # }


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BallotForm, self).__init__(*args, **kwargs)

        if self.instance.round.pairing.round_num == 5 or not self.instance.submit:
            for field in self.fields:
                self.fields[field].required = False
        if self.request.user.is_team:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True

        if self.request.user.is_judge and self.request.user.judge != self.instance.judge:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True

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
            team_ids = [person.pk for person in TeamMember.objects.filter(team=self.instance.round.p_team)] +\
                [person.pk for person in TeamMember.objects.filter(team=self.instance.round.d_team)]
            individual_award_query = TeamMember.objects.filter(pk__in=team_ids)
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
        self.init_ballot = kwargs.pop('ballot', None)
        self.init_subsection = kwargs.pop('subsection', None)
        super(BallotSectionForm, self).__init__(*args, **kwargs)
        if self.init_ballot:
            self.instance.ballot = self.init_ballot
        if self.init_subsection:
            self.instance.subsection = self.init_subsection
