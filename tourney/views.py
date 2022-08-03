import random
import string
import openpyxl
from ajax_select.fields import autoselect_fields_check_can_add
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from accounts.models import User
from tabeasy.settings import DEBUG
from tabeasy.utils.mixins import JudgeOnlyMixin, TeamOnlyMixin, AuthorizedJudgeOnlyMixin, PassRequestToFormViewMixin
from tabeasy_secrets.secret import DIVISION_ROUND_NUM
from tourney.forms import RoundForm, UpdateConflictForm, BallotForm, UpdateJudgeFriendForm, PairingFormSet, \
    CaptainsMeetingForm, PairingSubmitForm, JudgeForm
from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Round, Pairing, CaptainsMeeting
from tourney.models.team import Team, TeamMember

def sort_teams(teams):
    return list(reversed(sorted(teams,
                        key=lambda x: (x.total_ballots(), x.total_cs(), x.total_pd()))))

def index(request):
    return render(request, 'index.html')


@user_passes_test(lambda u: u.is_staff)
def results(request):
    div1_teams = sort_teams([team for team in Team.objects.filter(division='Disney')])
    div2_teams = sort_teams([team for team in Team.objects.filter(division='Universal')])
    dict = {'div1_teams_ranked': div1_teams,
            'div2_teams_ranked': div2_teams}
    return render(request, 'tourney/tab/results.html', dict)

@user_passes_test(lambda u: u.is_staff)
def individual_awards(request):
    atts_ranked = sorted([member for member in TeamMember.objects.all()],
                        key= lambda x: x.att_individual_score )
    wits_ranked = sorted([member for member in TeamMember.objects.all()],
                        key= lambda x: x.wit_individual_score)
    dict = {'atts_ranked': atts_ranked,
           'wits_ranked': wits_ranked,}
    return render(request, 'tourney/tab/individual_awards.html', dict)


@user_passes_test(lambda u: u.is_staff)
def next_pairing(request):
    teams = Team.objects.all()
    if Pairing.objects.exists():
        next_round = max([pairing.round_num for pairing in Pairing.objects.all()])+1
    else:
        next_round = 1
    if next_round % 2 == 0:
        div1_d_teams = sort_teams([team for team in Team.objects.filter(division='Disney')
                                   if team.next_side(next_round) == 'd'])
        div1_p_teams = sort_teams([team for team in Team.objects.filter(division='Disney')
                                   if team.next_side(next_round) == 'p'])
        div2_d_teams = sort_teams([team for team in Team.objects.filter(division='Universal')
                                   if team.next_side(next_round) == 'd'])
        div2_p_teams = sort_teams([team for team in Team.objects.filter(division='Universal')
                                   if team.next_side(next_round) == 'p'])
    else:
        div1_teams = sort_teams([team for team in Team.objects.filter(division='Disney')])
        div1_p_teams = []
        div1_d_teams = []
        for i in range(0, len(div1_teams), 2):
            if random.randint(0, 1):
                div1_p_teams.append(div1_teams[i])
                div1_d_teams.append(div1_teams[i+1])
            else:
                div1_p_teams.append(div1_teams[i+1])
                div1_d_teams.append(div1_teams[i])
        div2_teams = sort_teams([team for team in Team.objects.filter(division='Universal')])
        div2_p_teams = []
        div2_d_teams = []
        for i in range(0, len(div2_teams), 2):
            if random.randint(0, 1):
                div2_p_teams.append(div2_teams[i])
                div2_d_teams.append(div2_teams[i + 1])
            else:
                div2_p_teams.append(div2_teams[i + 1])
                div2_d_teams.append(div2_teams[i])

    dict = {'next_round': next_round,
            'divs': ['Disney','Universal'],
            'teams':[zip(div1_p_teams, div1_d_teams),
                     zip(div2_p_teams, div2_d_teams)]
            }
    return render(request, 'tourney/pairing/next_pairing.html', dict)

@user_passes_test(lambda u: u.is_staff)
def pairing_index(request):
    round_num_lists = sorted(Pairing.objects.values_list('round_num',flat=True).distinct())
    pairings = []
    for round_num in round_num_lists:
        pairings.append(Pairing.objects.filter(round_num=round_num).order_by('division'))
    if Pairing.objects.exists():
        next_round = max([pairing.round_num for pairing in Pairing.objects.all()]) + 1
    else:
        next_round = 1
    dict = {'pairings': pairings, 'next_round': next_round }
    return render(request, 'tourney/pairing/main.html', dict)

@user_passes_test(lambda u: u.is_staff)
def edit_pairing(request, round_num):
    if DEBUG:
        RoundFormSet = inlineformset_factory(Pairing, Round, form=RoundForm, formset=PairingFormSet,
                                             max_num=8, validate_max=True)
    else:
        RoundFormSet = inlineformset_factory(Pairing, Round, form=RoundForm, formset=PairingFormSet,
                                             max_num=8, validate_max=True,
                                             extra=8)
    autoselect_fields_check_can_add(RoundForm, Round, request.user)
    if not Pairing.objects.filter(round_num=round_num).exists():
        div1_pairing = Pairing.objects.create(round_num=round_num, division='Disney')
        div2_pairing = Pairing.objects.create(round_num=round_num, division='Universal')
    else:
        div1_pairing = Pairing.objects.filter(round_num=round_num).get(division='Disney')
        div2_pairing = Pairing.objects.filter(round_num=round_num).get(division='Universal')

    if request.method == "POST":
        div1_formset = RoundFormSet(request.POST, request.FILES, prefix='div1', instance=div1_pairing,
                                    form_kwargs={'pairing': div1_pairing})
        div2_formset = RoundFormSet(request.POST, request.FILES, prefix='div2', instance=div2_pairing,
                                    form_kwargs={'pairing': div2_pairing})

        div1_submit_form = PairingSubmitForm(request.POST, prefix='div1', instance=div1_pairing)
        div2_submit_form = PairingSubmitForm(request.POST, prefix='div2', instance=div2_pairing)
        if div1_submit_form.is_valid():
            div1_submit_form.save()
        if div2_submit_form.is_valid():
            div2_submit_form.save()
        both_true = True
        if div1_formset.is_valid():
            # get courtroom
            round_num = len(div1_formset)
            for form in div1_formset:
                if form.instance.p_team == None or form.instance.d_team == None:
                    round_num -= 1
            if div1_formset[0].instance.pairing.division == 'Disney':
                random_choice = string.ascii_uppercase[:DIVISION_ROUND_NUM][:round_num]
            else:
                random_choice = string.ascii_uppercase[DIVISION_ROUND_NUM:2 * DIVISION_ROUND_NUM][:round_num]
            random_choice = random.sample(list(random_choice), round_num)
            for i in range(len(div1_formset)):
                if div1_formset[i].instance.p_team != None and div1_formset[i].instance.d_team != None:
                    div1_formset[i].instance.courtroom = random_choice[i]
                    div1_formset[i].save()
            div1_formset.save()
        else:
            both_true = False

        if div2_formset.is_valid():
            round_num = len(div2_formset)
            for form in div2_formset:
                if form.instance.p_team == None or form.instance.d_team == None:
                    round_num -= 1
            if div2_formset[0].instance.pairing.division == 'Disney':
                random_choice = string.ascii_uppercase[:DIVISION_ROUND_NUM][:round_num]
            else:
                random_choice = string.ascii_uppercase[DIVISION_ROUND_NUM:2 * DIVISION_ROUND_NUM][:round_num]
            random_choice = random.sample(list(random_choice), round_num)
            for i in range(len(div2_formset)):
                if div2_formset[i].instance.p_team != None and div2_formset[i].instance.d_team != None:
                    div2_formset[i].instance.courtroom = random_choice[i]
                    div2_formset[i].save()
            div2_formset.save()
        else:
            both_true = False

        if both_true:
            return redirect('tourney:pairing_index')
    else:
        div1_formset = RoundFormSet(instance=div1_pairing,prefix='div1', form_kwargs={'pairing': div1_pairing})
        div2_formset = RoundFormSet(instance=div2_pairing,prefix='div2', form_kwargs={'pairing': div2_pairing})
        div1_submit_form = PairingSubmitForm(instance=div1_pairing, prefix='div1')
        div2_submit_form = PairingSubmitForm(instance=div2_pairing, prefix='div2')
    available_judges_pk = [judge.pk for judge in Judge.objects.all()
                           if judge.get_availability(div1_pairing.round_num)]
    return render(request, 'tourney/pairing/edit.html', {'formsets': [div1_formset, div2_formset],
                                                         'div1_submit_form': div1_submit_form,
                                                         'div2_submit_form': div2_submit_form,
                                                         'pairing': div1_pairing,
                                                         'judges': Judge.objects.filter(pk__in=available_judges_pk)})


@user_passes_test(lambda u: u.is_staff)
def delete_pairing(request, round_num):
    if Pairing.objects.filter(round_num=round_num).exists():
        Pairing.objects.filter(round_num=round_num).delete()
    return redirect('tourney:pairing_index')

@user_passes_test(lambda u: u.is_staff)
def view_ballot_status(request, pairing_id):
    pairing = Pairing.objects.get(pk=pairing_id)
    ballots = []
    for round in pairing.rounds.all():
        for ballot in round.ballots.all():
            ballots.append(ballot)
    ballots = sorted(ballots, key=lambda x: x.round.courtroom)
    return render(request, 'tourney/tab/view_ballots_status.html', {'ballots': ballots})
# @login_required
# # def add_conflict(request):
# #     if request.method == 'POST':
# #         form = AddConflictForm(data=request.POST)
# #         if form.is_valid():
# #
# #     return render(request, 'tourney/add_conflict.html', {'form':form})

class ConflictUpdateView(JudgeOnlyMixin, UpdateView):
    model = Judge
    template_name = "tourney/add_conflict.html"

    form_class = UpdateConflictForm

    def get_form(self, form_class=None):
        form = super(ConflictUpdateView, self).get_form(form_class)
        form.fields['conflicts'].required = False
        return form

    def get_object(self, queryset=None):
        return self.request.user.judge

    success_url = reverse_lazy('index')

class JudgeFriendUpdateView(JudgeOnlyMixin, UpdateView):
    model = Judge
    template_name = "utils/generic_form.html"

    form_class = UpdateJudgeFriendForm

    def get_form(self, form_class=None):
        form = super(JudgeFriendUpdateView, self).get_form(form_class)
        form.fields['judge_friends'].required = False
        return form

    def get_object(self, queryset=None):
        return self.request.user.judge

    success_url = reverse_lazy('index')

class JudgePreferenceUpdateView(JudgeOnlyMixin, UpdateView):
    model = Judge
    template_name = "utils/generic_form.html"

    form_class = JudgeForm

    def get_object(self, queryset=None):
        return self.request.user.judge

    success_url = reverse_lazy('index')


class BallotUpdateView(PassRequestToFormViewMixin, LoginRequiredMixin, UpdateView):
    model = Ballot
    template_name = "tourney/ballot.html"
    form_class = BallotForm
    permission_denied_message = 'You are not allowed to view this ballot.'

    def test_func(self):
        if not super().test_func():
            return False
        self.ballot = get_object_or_404(Ballot, pk=self.kwargs['pk'])
        if self.ballot.judge != self.request.user.judge \
                and self.request.user.team not in self.captains_meeting.round.teams:
            return False
        return True

    def get_success_url(self):
        return self.request.path

class CaptainsMeetingUpdateView(PassRequestToFormViewMixin, LoginRequiredMixin, UpdateView):
    model = CaptainsMeeting
    template_name = "tourney/captains_meeting.html"
    form_class = CaptainsMeetingForm
    permission_denied_message = 'You are not allowed to view this Captains Meeting Form.'

    def test_func(self):
        if not super().test_func():
            return False
        self.captains_meeting = get_object_or_404(CaptainsMeeting, pk=self.kwargs['pk'])
        if self.request.user.team not in self.captains_meeting.round.teams and \
                self.request.user.judge not in self.captains_meeting.round.judges:
            return False
        return True

    def get_success_url(self):
        return reverse_lazy('index')

@user_passes_test(lambda u: u.is_staff)
def load_teams(request):
    if "GET" == request.method:
        return render(request, 'admin/load_excel.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Teams"]
        list = []
        n = worksheet.max_row
        m = worksheet.max_column
        for i in range(2, n + 1):
            pk = worksheet.cell(i, 1).value
            if pk is None:
                continue
            pk = int(pk)
            team_name = worksheet.cell(i, 2).value
            division = worksheet.cell(i, 3).value
            school = worksheet.cell(i, 4).value
            j = 5
            team_roster = []
            while j <= m and worksheet.cell(i,j).value != None and worksheet.cell(i,j).value != '':
                team_roster.append(worksheet.cell(i,j).value)
                j+=1
            message = ''
            if len(team_roster) < 6:
                message += f' errors: team {pk} less than 6 members '
            elif len(team_roster) > 10:
                message += f' errors: team {pk} more than 10 members '
            else:
                try:
                    if Team.objects.filter(pk=pk).exists():
                        message += f'update team {pk}'
                        Team.objects.filter(pk=pk).update(team_name=team_name,division=division,school=school)
                    else:
                        message += f'create team {pk}'
                        raw_password = worksheet.cell(i,17).value
                        username = ''.join(team_name.split(' '))
                        user = User(username=username, raw_password=raw_password, is_team=True, is_judge=False)
                        user.set_password(raw_password)
                        user.save()
                        Team.objects.create(team_id=pk, user=user, team_name=team_name,division=division,school=school)
                    for name in team_roster:
                        if TeamMember.objects.filter(name=name).exists():
                            message += f'update member {name}'
                            TeamMember.objects.filter(name=name).update(team=Team.objects.filter(pk=pk)[0],name=name)
                        else:
                            message += f'create member {name}'
                            TeamMember.objects.create(name=name,team=Team.objects.filter(pk=pk)[0])
                except Exception as e:
                    message += str(e)
                else:
                    message += 'success'
            list.append(message)
        return render(request, 'admin/load_excel.html', {"list": list})



@user_passes_test(lambda u: u.is_staff)
def load_judges(request):
    if "GET" == request.method:
        return render(request, 'admin/load_excel.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]
        list = []
        n = worksheet.max_row
        m = worksheet.max_column
        for i in range(2, n + 1):
            username = worksheet.cell(i, 9).value
            first_name = worksheet.cell(i, 1).value
            last_name = worksheet.cell(i, 2).value
            if last_name == None or last_name == '':
                last_name = ' '
            raw_password = worksheet.cell(i,10).value
            preside = worksheet.cell(i,3).value
            if preside == 'CIN':
                preside = 2
            elif preside == 'y':
                preside = 1
            else:
                preside = 0
            availability = []
            for j in range(4, 8):
                if worksheet.cell(i, j).value == 'y':
                    availability.append(True)
                else:
                    availability.append(False)

            message = ''
            try:
                if Judge.objects.filter(user__username=username).exists():
                    message += f'update judge {username}'
                    judge = Judge.objects.get(user__username=username)
                    user = judge.user
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    judge.preside = preside
                    for i in range(len(availability)):
                        setattr(judge, f'available_round{i+1}', availability[i])
                    judge.save()

                else:
                    message += f'create judge {username}'
                    user = User(username=username, raw_password=raw_password,
                                first_name=first_name, last_name=last_name,
                                is_team=False, is_judge=True)
                    user.set_password(raw_password)
                    user.save()
                    judge = Judge(user=user, preside=preside)
                    for i in range(len(availability)):
                        setattr(judge, f'available_round{i+1}', availability[i])
                    judge.save()

            except Exception as e:
                message += str(e)
            else:
                message += 'success'
            list.append(message)
        return render(request, 'admin/load_excel.html', {"list": list})