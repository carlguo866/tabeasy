from django.core.exceptions import ValidationError
from django.db import models
import uuid
from tourney.models.competitor import Competitor
from tourney.models.tournament import Tournament


class CaptainsMeeting(models.Model):
    round = models.OneToOneField('tourney.Round', on_delete=models.CASCADE, related_name='captains_meeting'
                                 , related_query_name='captains_meeting', primary_key=True)
    #
    # character_evidence_option1 = models.BooleanField(default=False, help_text='The defendant will offer evidence under MRE 404(a)(1) of the following traits of his/her own character:')
    # character_evidence_option1_description = models.CharField(max_length=40, default='')
    # character_evidence_option2 = models.BooleanField(default=False,
    #                                                  help_text='The defendant will offer evidence under MRE 404(a)(2) of the following traits of the victim(s)\' character:')
    # character_evidence_option2_description = models.CharField(max_length=40, default='')
    # character_evidence_option3 = models.BooleanField(default=False,
    #                                                  help_text='The prosecutor will offer evidence of prior crimes, wrongs, or acts under MRE 404(b) for the following purposes:')
    # character_evidence_option3_description = models.CharField(max_length=40, default='')
    # character_evidence_option4 = models.BooleanField(default=False,
    #                                                  help_text='The defense will attack, by reputation or opinion, credibility of the following witnesses called by the prosecution under MRE 608(a)')
    # character_evidence_option4_description = models.CharField(max_length=40, default='')
    # character_evidence_submit = models.BooleanField(default=False,
    #                                          help_text='Was Character Evidence form completed?')
    #
    # def character_evidence_options(self):
    #     return [self.character_evidence_option1,self.character_evidence_option2,
    #             self.character_evidence_option3,self.character_evidence_option4]
    #
    #
    # p_charge_options = [
    #     ('Haley Floyd','Haley Floyd'),
    #     ('Winston Thomas','Winston Thomas'),
    #     ('Both victims','Both victims')
    # ]
    # p_charge = models.CharField(max_length=30, choices=p_charge_options, null=True)
    #
    # d_charge_options = [
    #     ('not_guilty','Not guilty of all criminal charges.'),
    #     ('not_guilty_robbery_1','Not guilty of ROBBERY 1 but guilty of ROBBERY 2 and THEFT BY DECEPTION.'),
    #     ('not_guilty_robbery','Not guilty of ROBBERY but guilty of THEFT BY DECEPTION'),
    # ]
    # d_charge = models.CharField(max_length=30, choices=d_charge_options, null=True)
    #
    #
    # witness_choices = [
    #     ('J.C. Longstreet' , 'J.C. Longstreet' ),
    #     ('Francis Kimball', 'Francis Kimball'),
    #     ('Whit Bowman', 'Whit Bowman'),
    #     ('Jackie Hunter', 'Jackie Hunter'),
    #     ('Charlie Kaminsky', 'Charlie Kaminsky'),
    #     ('Billy Isaacs', 'Billy Isaacs'),
    #     ('Haley Floyd', 'Haley Floyd'),
    # ]
    # p_opener = models.ForeignKey(Competitor, on_delete=models.SET_NULL,
    #                              related_name='p_opener', related_query_name='p_opener', null=True)
    # d_opener = models.ForeignKey(Competitor, on_delete=models.SET_NULL, related_name='d_opener', null=True)
    # #
    # p_wit1_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    # p_wit1 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_wit1', null=True)
    # p_wit1_direct_att = models.ForeignKey(Competitor, on_delete=models.CASCADE,
    #                                       related_name='p_wit1_direct_att', null=True)
    # p_wit1_cross_att = models.ForeignKey(Competitor, on_delete=models.CASCADE,
    #                                      related_name='p_wit1_cross_att', null=True)
    #
    # p_wit2_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    # p_wit2 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_wit2', null=True)
    # p_wit2_direct_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_wit2_direct_att',
    #                                       null=True)
    # p_wit2_cross_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_wit2_cross_att',
    #                                      null=True)
    #
    # p_wit3_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    # p_wit3 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_wit3', null=True)
    # p_wit3_direct_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_wit3_direct_att',
    #                                       null=True)
    # p_wit3_cross_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_wit3_cross_att',
    #                                      null=True)
    #
    #
    # d_wit1_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    # d_wit1 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_wit1', null=True)
    # d_wit1_direct_att = models.ForeignKey(Competitor, on_delete=models.CASCADE,
    #                                       related_name='d_wit1_direct_att', null=True)
    # d_wit1_cross_att = models.ForeignKey(Competitor, on_delete=models.CASCADE,
    #                                      related_name='d_wit1_cross_att', null=True)
    #
    # d_wit2_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    # d_wit2 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_wit2', null=True)
    # d_wit2_direct_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_wit2_direct_att',
    #                                       null=True)
    # d_wit2_cross_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_wit2_cross_att',
    #                                      null=True)
    #
    # d_wit3_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    # d_wit3 = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_wit3', null=True)
    # d_wit3_direct_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_wit3_direct_att',
    #                                       null=True)
    # d_wit3_cross_att = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_wit3_cross_att',
    #                                      null=True)
    #
    # p_closer = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='p_closer', null=True)
    # d_closer = models.ForeignKey(Competitor, on_delete=models.CASCADE, related_name='d_closer', null=True)
    #
    # @property
    # def p_direct_atts(self):
    #     return [self.p_wit1_direct_att,self.p_wit2_direct_att, self.p_wit3_direct_att]
    #
    # @property
    # def d_direct_atts(self):
    #     return [self.d_wit1_direct_att, self.d_wit2_direct_att, self.d_wit3_direct_att]
    #
    # @property
    # def p_cross_atts(self):
    #     return [self.d_wit1_cross_att, self.d_wit2_cross_att, self.d_wit3_cross_att]
    #
    # @property
    # def d_cross_atts(self):
    #     return [self.p_wit1_cross_att, self.p_wit2_cross_att, self.p_wit3_cross_att]
    #
    # @property
    # def atts(self):
    #     return self.p_direct_atts + self.d_direct_atts
    #
    # @property
    # def p_wits(self):
    #     return [self.p_wit1, self.p_wit2, self.p_wit3]
    #
    # @property
    # def d_wits(self):
    #     return [self.d_wit1, self.d_wit2, self.d_wit3]
    #
    # @property
    # def wits(self):
    #     return self.p_wits + self.d_wits
    #
    # def p_characters(self):
    #     return [self.p_wit1_name, self.p_wit2_name, self.p_wit3_name]
    #
    # def d_characters(self):
    #     return [self.d_wit1_name, self.d_wit2_name, self.d_wit3_name]
    #
    # def characters(self):
    #     return self.p_characters()+ self.d_characters()

    demo = models.BooleanField(default=False, help_text='Were all exhibits/demonstratives shown to opposing counsel?')
    submit =  models.BooleanField(default=False, help_text='Submit')

    def __str__(self):
        return f"{self.round} {self.round.p_team} vs. {self.round.d_team}"

    def clean(self):
        errors = []

        if self.submit:
            #
            # fields = [f.name for f in self._meta.get_fields()]
            # model_fields = [( getattr(self, field_name), field_name) for field_name in fields]
            # for field, field_name in model_fields:
            #     if field == None:
            #         errors.append(f"You have not entered any values in {field_name}")

            # for i, character_evidence_option in enumerate(self.character_evidence_options()):
            #     if character_evidence_option and \
            #             getattr(self, f"character_evidence_option{i+1}_description") == '':
            #         errors.append(f'You filled out Character Evidence Option {i+1} as yes, but you didn\'t provide description.')

            # if not self.character_evidence_submit:
            #     errors.append('You didn\'t submit the Character Evidence Form!')

            # # characters
            # characters = []
            # for x in self.sections.all():
            #     if captains_meeting_subsection.subsection.type == 'direct' and \
            #         captains_meeting_subsection.subsection.role == 'wit':
            #         characters.append(captains_meeting_subsection.character)


            # if len(self.characters()) !=  len(set(self.characters())):
            #     errors.append("Each witness can only be called once")
            # for character in self.p_characters():
            #     if character not in ['J.C. Longstreet', 'Francis Kimball', 'Charlie Kaminsky','Billy Isaacs','Haley Floyd']:
            #         errors.append(f"{character} cannot be called by the Prosecution")
            # for character in self.d_characters():
            #     if character not in ['Whit Bowman', 'Jackie Hunter', 'Charlie Kaminsky','Billy Isaacs','Haley Floyd']:
            #         errors.append(f"{character} cannot be called by the Defense")
            # #p
            # if self.p_opener == self.p_closer:
            #     errors.append(f"{self.p_opener} cannot give both Opening Statement and Closing Argument")
            # if len(self.p_direct_atts) != len(set(self.p_direct_atts)):
            #     errors.append(f"Prosecution has one attorney assigned for two Direct Examinations")
            # if len(self.p_cross_atts) != len(set(self.p_cross_atts)):
            #     errors.append(f"Prosecution has one attorney assigned for two Cross Examinations")
            # if len(self.p_wits) != len(set(self.p_wits)):
            #     errors.append(f"Prosecution has one witness assigned for two characters")
            #
            # if sorted(self.p_direct_atts) != sorted(self.p_cross_atts):
            #     errors.append(f"{sorted(self.p_direct_atts)} cross and direct not the same three ppl")
            #
            # #d
            # if self.d_opener == self.d_closer:
            #     errors.append(f"{self.d_opener} cannot give both Opening Statement and Closing Argument")
            # if len(self.d_direct_atts) != len(set(self.d_direct_atts)):
            #     errors.append(f"Defense has one attorney assigned for two Direct Examinations")
            # if len(self.d_cross_atts) != len(set(self.d_cross_atts)):
            #     errors.append(f"Defense has one attorney assigned for two Cross Examinations")
            # if len(self.d_wits) != len(set(self.d_wits)):
            #     errors.append(f"Defense has one witness assigned for two characters")
            # if self.d_direct_atts != None \
            #         and self.p_direct_atts != None \
            #         and sorted(self.d_direct_atts) != sorted(self.d_cross_atts):
            #     errors.append(f"Each team must have exactly three attorneys each round")
            #
            # for wit in self.wits:
            #     if wit in self.atts:
            #         errors.append(f"{wit} assigned as both an attorney and witness")

            if not self.demo:
                errors.append('You didn\'t check for demo')

        if errors != []:
            raise ValidationError(errors)


