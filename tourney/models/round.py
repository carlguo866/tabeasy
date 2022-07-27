from annoying.fields import AutoOneToOneField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# Create your models here
from django_better_admin_arrayfield.models.fields import ArrayField
from tourney.models.team import Team, TeamMember


class Pairing(models.Model):
    division_choices = [('Disney', 'Disney'), ('Universal', 'Universal')]
    division = models.CharField(
        max_length=100,
        choices=division_choices
    )
    round_num = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('division', 'round_num',)

    def __str__(self):
        return f'Round {self.round_num}'

class Round(models.Model):
    pairing = models.ForeignKey(Pairing, on_delete=models.CASCADE, related_name='rounds', related_query_name='round', null=True)
    courtroom = models.CharField(max_length=1, null=True)
    p_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='p_rounds',
                               related_query_name='p_round', null=True)
    d_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='d_rounds',
                               related_query_name='d_round', null=True)
    judges = models.ManyToManyField('Judge', related_name='rounds',
                                    related_query_name='round',
                                    through='Ballot')
    def __str__(self):
        return f'Round {self.pairing.round_num} Courtroom {self.courtroom.upper()}'

    def save(self, force_insert=False, force_update=False):
        is_new = self.id is None
        super(Round, self).save(force_insert, force_update)
        if is_new:
            CaptainsMeeting.objects.create(round=self)
    # def clean(self, *args, **kwargs):
    #
    #     super().clean()




class CaptainsMeeting(models.Model):
    round = models.OneToOneField(Round, on_delete=models.CASCADE, related_name='captains_meeting'
                                 , related_query_name='captains_meeting', primary_key=True)
    character_evidence = models.BooleanField(default=False, null=True,
                                             help_text='Was Character Evidence form completed?')
    p_charge_options = [
        ('Haley Floyd','Haley Floyd'),
        ('Winston Thomas','Winston Thomas'),
        ('Both victims','Both victims')
    ]
    p_charge = models.CharField(max_length=30, choices=p_charge_options, null=True, blank=True)

    d_charge_options = [
        ('not_guilty','Not guilty of all criminal charges.'),
        ('not_guilty_robbery_1','Not guilty of ROBBERY 1 but guilty of ROBBERY 2 and THEFT BY DECEPTION.'),
        ('not_guilty_robbery','Not guilty of ROBBERY but guilty of THEFT BY DECEPTION'),
    ]
    d_charge = models.CharField(max_length=30, choices=d_charge_options, null=True, blank=True)


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
                                 related_name='p_opener', related_query_name='p_opener', null=True, blank=True)
    d_opener = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, related_name='d_opener', null=True, blank=True)
    #
    p_wit1_name = models.CharField(max_length=30, choices=witness_choices, null=True, blank=True)
    p_wit1 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit1', null=True, blank=True)
    p_wit1_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                          related_name='p_wit1_direct_att', null=True, blank=True)
    p_wit1_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                         related_name='p_wit1_cross_att', null=True, blank=True)

    p_wit2_name = models.CharField(max_length=30, choices=witness_choices, null=True, blank=True)
    p_wit2 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit2', null=True, blank=True)
    p_wit2_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit2_direct_att',
                                          null=True, blank=True)
    p_wit2_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit2_cross_att',
                                         null=True, blank=True)

    p_wit3_name = models.CharField(max_length=30, choices=witness_choices, null=True, blank=True)
    p_wit3 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit3', null=True, blank=True)
    p_wit3_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit3_direct_att',
                                          null=True, blank=True)
    p_wit3_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_wit3_cross_att',
                                         null=True, blank=True)


    d_wit1_name = models.CharField(max_length=30, choices=witness_choices, null=True, blank=True)
    d_wit1 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit1', null=True, blank=True)
    d_wit1_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                          related_name='d_wit1_direct_att', null=True, blank=True)
    d_wit1_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE,
                                         related_name='d_wit1_cross_att', null=True, blank=True)

    d_wit2_name = models.CharField(max_length=30, choices=witness_choices, null=True, blank=True)
    d_wit2 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit2', null=True, blank=True)
    d_wit2_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit2_direct_att',
                                          null=True, blank=True)
    d_wit2_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit2_cross_att',
                                         null=True, blank=True)

    d_wit3_name = models.CharField(max_length=30, choices=witness_choices, null=True, blank=True)
    d_wit3 = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit3', null=True, blank=True)
    d_wit3_direct_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit3_direct_att',
                                          null=True, blank=True)
    d_wit3_cross_att = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_wit3_cross_att',
                                         null=True, blank=True)

    p_closer = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='p_closer', null=True, blank=True)
    d_closer = models.ForeignKey(TeamMember, on_delete=models.CASCADE, related_name='d_closer', null=True, blank=True)

    demo = models.BooleanField(default=False, null=True,
                                             help_text='Were all exhibits/demonstratives shown to opposing counsel?')
    submit =  models.BooleanField(default=False, null=True, help_text='Submit')
