from django.core.exceptions import ValidationError
from django.db import models

from tourney.models import TeamMember


class CaptainsMeeting(models.Model):
    round = models.OneToOneField('Round', on_delete=models.CASCADE, related_name='captains_meeting'
                                 , related_query_name='captains_meeting', primary_key=True)

    character_evidence_option1 = models.BooleanField(default=False, help_text='The defendant will offer evidence of his/her own character or trait of character [404(a)(1)].')
    character_evidence_option2 = models.BooleanField(default=False,
                                                     help_text='The defendant will offer evidence of the victim\'s character or trait of character [404(a)(2)].')
    character_evidence_option3 = models.BooleanField(default=False,
                                                     help_text='The prosecutor will offer evidence of prior crimes, wrongs, or acts [404(b)].')
    character_evidence_option4 = models.BooleanField(default=False,
                                                     help_text='The defense will offer opinion and/or reputation evidence of character [608(a)].')
    character_evidence_submit = models.BooleanField(default=False,
                                             help_text='Was Character Evidence form completed?')

    p_charge_options = [
        ('Haley Floyd','Haley Floyd'),
        ('Winston Thomas','Winston Thomas'),
        ('Both victims','Both victims')
    ]
    p_charge = models.CharField(max_length=30, choices=p_charge_options, null=True)

    d_charge_options = [
        ('not_guilty','Not guilty of all criminal charges.'),
        ('not_guilty_robbery_1','Not guilty of ROBBERY 1 but guilty of ROBBERY 2 and THEFT BY DECEPTION.'),
        ('not_guilty_robbery','Not guilty of ROBBERY but guilty of THEFT BY DECEPTION'),
    ]
    d_charge = models.CharField(max_length=30, choices=d_charge_options, null=True)


    witness_choices = [
        ('J.C. Longstreet' , 'J.C. Longstreet' ),
        ('Francis Kimball', 'Francis Kimball'),
        ('Whit Bowman', 'Whit Bowman'),
        ('Jackie Hunter', 'Jackie Hunter'),
        ('Charlie Kaminsky', 'Charlie Kaminsky'),
        ('Billy Isaacs', 'Billy Isaacs'),
        ('Haley Floyd', 'Haley Floyd'),
    ]
    p_opener = models.ForeignKey(TeamMember, on_delete=models.SET_NULL,
                                 related_name='p_opener', related_query_name='p_opener', null=True)
    d_opener = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, related_name='d_opener', null=True)
    #
    p_wit1_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    p_wit1 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit1', null=True)
    p_wit1_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                          related_name='p_wit1_direct_att', null=True)
    p_wit1_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                         related_name='p_wit1_cross_att', null=True)

    p_wit2_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    p_wit2 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit2', null=True)
    p_wit2_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit2_direct_att',
                                          null=True)
    p_wit2_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit2_cross_att',
                                         null=True)

    p_wit3_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    p_wit3 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit3', null=True)
    p_wit3_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit3_direct_att',
                                          null=True)
    p_wit3_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit3_cross_att',
                                         null=True)


    d_wit1_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    d_wit1 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit1', null=True)
    d_wit1_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                          related_name='d_wit1_direct_att', null=True)
    d_wit1_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                         related_name='d_wit1_cross_att', null=True)

    d_wit2_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    d_wit2 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit2', null=True)
    d_wit2_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit2_direct_att',
                                          null=True)
    d_wit2_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit2_cross_att',
                                         null=True)

    d_wit3_name = models.CharField(max_length=30, choices=witness_choices, null=True)
    d_wit3 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit3', null=True)
    d_wit3_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit3_direct_att',
                                          null=True)
    d_wit3_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit3_cross_att',
                                         null=True)

    p_closer = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_closer', null=True)
    d_closer = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_closer', null=True)

    @property
    def p_direct_atts(self):
        return [self.p_wit1_direct_att,self.p_wit2_direct_att, self.p_wit3_direct_att]

    @property
    def d_direct_atts(self):
        return [self.d_wit1_direct_att, self.d_wit2_direct_att, self.d_wit3_direct_att]

    @property
    def p_cross_atts(self):
        return [self.d_wit1_cross_att, self.d_wit2_cross_att, self.d_wit3_cross_att]

    @property
    def d_cross_atts(self):
        return [self.p_wit1_cross_att, self.p_wit2_cross_att, self.p_wit3_cross_att]

    @property
    def atts(self):
        return self.p_direct_atts + self.d_direct_atts

    @property
    def p_wits(self):
        return [self.p_wit1, self.p_wit2, self.p_wit3]

    @property
    def d_wits(self):
        return [self.d_wit1, self.d_wit2, self.d_wit3]

    @property
    def wits(self):
        return self.p_wits + self.d_wits

    def p_characters(self):
        return [self.p_wit1_name, self.p_wit2_name, self.p_wit3_name]

    def d_characters(self):
        return [self.d_wit1_name, self.d_wit2_name, self.d_wit3_name]

    def characters(self):
        return self.p_characters()+ self.d_characters()

    pronouns = [
        ('he', 'He/Him'),
        ('she', 'She/Her'),
        ('they','They/Them'),
        ('ze','Ze/Hir')
    ]

    longstreet_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='J.C. Longstreet Pronoun')
    kimball_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='Francis Kimball Pronoun')
    bowman_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='Whit Bowman Pronoun')
    hunter_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='Jackie Hunter Pronoun')
    kaminsky_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='Charlie Kaminsky Pronoun')
    isaacs_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='Billie Issacs Pronoun')
    floyd_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='Haley Floyd Pronoun')
    poole_pronoun = models.CharField(max_length=30, choices=pronouns, null=True, help_text='Cameron Poole Pronoun')

    demo = models.BooleanField(default=False, help_text='Were all exhibits/demonstratives shown to opposing counsel?')
    submit =  models.BooleanField(default=False, help_text='Submit')

    def clean(self):
        errors = []
        if self.submit:
            #characters
            if not self.character_evidence_submit:
                errors.append('didn\'t submit character evidence')
            if len(self.characters()) !=  len(set(self.characters())):
                errors.append("a character used twice")
            for character in self.p_characters():
                if character not in ['J.C. Longstreet', 'Francis Kimball', 'Charlie Kaminsky','Billy Isaacs','Haley Floyd']:
                    errors.append(f"{character} not supposed to be used by p")
            for character in self.d_characters():
                if character not in ['Whit Bowman', 'Jackie Hunter', 'Charlie Kaminsky','Billy Isaacs','Haley Floyd']:
                    errors.append(f"{character} not supposed to be used by d")

            if len(self.p_direct_atts) != len(set(self.p_direct_atts)):
                errors.append(f"p has one attorneys for two directs")
            if len(self.p_cross_atts) != len(set(self.p_cross_atts)):
                errors.append(f"p has one attorneys for two crosses")
            if sorted(self.p_direct_atts) != sorted(self.p_cross_atts):
                errors.append(f"{sorted(self.p_direct_atts)} cross and direct not the same three ppl")

            if len(self.d_direct_atts) != len(set(self.d_direct_atts)):
                errors.append(f"d has one attorneys for two directs")
            if len(self.d_cross_atts) != len(set(self.d_cross_atts)):
                errors.append(f"d has one attorneys for two crosses")
            if sorted(self.d_direct_atts) != sorted(self.d_cross_atts):
                errors.append(f"{sorted(self.d_direct_atts)} cross and direct not the same three ppl")

            for wit in self.wits:
                if wit in self.atts:
                    errors.append(f"{wit} both attorney and witness")

            if not self.demo:
                errors.append('didn\'t check demo')

        if errors != []:
            raise ValidationError(errors)