import random
import string
import openpyxl
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.models import User
from submission.forms import CharacterPronounsForm
from submission.models.section import Section, SubSection
from tabeasy.settings import DEBUG
from tabeasy.utils.mixins import JudgeOnlyMixin, PassRequestToFormViewMixin
from tabeasy_secrets.secret import  str_int
from tourney.forms import RoundForm, UpdateConflictForm, UpdateJudgeFriendForm, PairingFormSet, PairingSubmitForm, \
    JudgeForm, CheckinJudgeForm, CompetitorPronounsForm
from submission.models.ballot import Ballot
from submission.models.character import Character, CharacterPronouns
from tourney.models.judge import Judge
from tourney.models.round import Round, Pairing
from tourney.models.team import Team
from tourney.models.competitor import Competitor

def sort_teams(teams):
    return list(reversed(sorted(teams,
                        key=lambda x: (x.total_ballots(), x.total_cs(), x.total_pd()))))

def index(request):
    return render(request, 'index.html')


@user_passes_test(lambda u: u.is_staff)
def results(request):
    tournament = request.user.tournament
    if tournament.split_division:
        div1_teams = sort_teams([team for team in Team.objects.filter(division='Disney')])
        div2_teams = sort_teams([team for team in Team.objects.filter(division='Universal')])
        dict = {'teams_ranked': [div1_teams, div2_teams]}
    else:
        teams = sort_teams([team for team in Team.objects.filter(user__tournament=tournament)])
        dict = {'teams_ranked': [teams]}
    return render(request, 'tourney/tab/results.html', dict)

@user_passes_test(lambda u: u.is_staff)
def individual_awards(request):
    tournament = request.user.tournament
    atts_ranked = [(member,'P',member.att_individual_score()[0]) for member in Competitor.objects.filter(team__user__tournament=tournament)
                   if member.att_individual_score()[0] >= 10]+ \
                  [(member, 'D', member.att_individual_score()[1]) for member in Competitor.objects.filter(team__user__tournament=tournament)
                   if member.att_individual_score()[1] >= 10]
    atts_ranked = sorted(atts_ranked, key=lambda x: -x[2])
    wits_ranked = [(member,'P',member.wit_individual_score()[0]) for member in Competitor.objects.filter(team__user__tournament=tournament)
                   if member.wit_individual_score()[0] >= 10]+ \
                  [(member, 'D', member.wit_individual_score()[1]) for member in Competitor.objects.filter(team__user__tournament=tournament)
                   if member.wit_individual_score()[1] >= 10]
    wits_ranked = sorted(wits_ranked, key=lambda x: -x[2])

    dict = {'ranked': zip(atts_ranked,wits_ranked)}
    return render(request, 'tourney/tab/individual_awards.html', dict)


@user_passes_test(lambda u: u.is_staff)
def next_pairing(request):
    tournament = request.user.tournament
    if Pairing.objects.filter(tournament=tournament).exists():
        next_round = max([pairing.round_num for pairing in Pairing.objects.filter(tournament=tournament)])+1
    else:
        next_round = 1

    if tournament.split_division:
        if next_round % 2 == 0:
            i_d_teams = sort_teams([team for team in Team.objects.filter(division='Disney')
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
    else:
        if next_round % 2 == 0:
            d_teams = sort_teams([team for team in Team.objects.filter(user__tournament=tournament)
                                       if team.next_side(next_round) == 'd'])
            p_teams = sort_teams([team for team in Team.objects.filter(user__tournament=tournament)
                                       if team.next_side(next_round) == 'p'])
        else:
            teams = sort_teams([team for team in Team.objects.filter(user__tournament=tournament)])
            p_teams = []
            d_teams = []
            for i in range(0, len(teams), 2):
                if random.randint(0, 1):
                    p_teams.append(teams[i])
                    d_teams.append(teams[i + 1])
                else:
                    p_teams.append(teams[i + 1])
                    d_teams.append(teams[i])
        dict = {'next_round': next_round,
                'divs': ['Teams'],
                'teams': [zip(p_teams, d_teams)]
                }
    return render(request, 'tourney/pairing/next_pairing.html', dict)

@user_passes_test(lambda u: u.is_staff)
def pairing_index(request):
    tournament = request.user.tournament
    round_num_lists = sorted(Pairing.objects.filter(tournament=tournament).values_list('round_num',flat=True).distinct())
    pairings = []
    for round_num in round_num_lists:
        pairings.append(Pairing.objects.filter(tournament=tournament,
                                               round_num=round_num).order_by('division'))
    if Pairing.objects.filter(tournament=tournament).exists():
        next_round = max([pairing.round_num for pairing in Pairing.objects.filter(tournament=tournament)]) + 1
    else:
        next_round = 1
    dict = {'pairings': pairings, 'next_round': next_round }
    return render(request, 'tourney/pairing/main.html', dict)

@user_passes_test(lambda u: u.is_staff)
def edit_pairing(request, round_num):
    tournament = request.user.tournament
    if DEBUG:
        RoundFormSet = inlineformset_factory(Pairing, Round, form=RoundForm, formset=PairingFormSet,
                                             max_num=int(tournament.division_team_num/2), validate_max=True,
                                             extra=int(tournament.division_team_num/2))
    else:
        RoundFormSet = inlineformset_factory(Pairing, Round, form=RoundForm, formset=PairingFormSet,
                                             max_num=int(tournament.division_team_num/2), validate_max=True,
                                             extra=int(tournament.division_team_num/2))

    if request.user.tournament.split_division:
        if not Pairing.objects.filter(round_num=round_num).exists():
            div1_pairing = Pairing.objects.create(round_num=round_num, division='Disney')
            div2_pairing = Pairing.objects.create(round_num=round_num, division='Universal')
        else:
            div1_pairing = Pairing.objects.filter(round_num=round_num).get(division='Disney')
            div2_pairing = Pairing.objects.filter(round_num=round_num).get(division='Universal')

        available_judges_pk = [judge.pk for judge in Judge.objects.all()
                               if judge.get_availability(div1_pairing.round_num)]
        judges = Judge.objects.filter(pk__in=available_judges_pk).order_by('-checkin','-preside', 'user__username').all()

        if request.method == "POST":
            div1_formset = RoundFormSet(request.POST, request.FILES, prefix='div1', instance=div1_pairing,
                                        form_kwargs={'pairing': div1_pairing, 'other_formset':None, 'request':request })
            div2_formset = RoundFormSet(request.POST, request.FILES, prefix='div2', instance=div2_pairing,
                                        form_kwargs={'pairing': div2_pairing, 'other_formset':div1_formset, 'request':request })

            div1_submit_form = PairingSubmitForm(request.POST, prefix='div1', instance=div1_pairing)
            div2_submit_form = PairingSubmitForm(request.POST, prefix='div2', instance=div2_pairing)

            if div1_submit_form.is_valid():
                div1_submit_form.save()
            if div2_submit_form.is_valid():
                div2_submit_form.save()
            both_true = True
            if div1_formset.is_valid():
                # get courtroom
                actual_round_num = len(div1_formset)
                for form in div1_formset:
                    if form.instance.p_team == None or form.instance.d_team == None:
                        actual_round_num -= 1
                if div1_formset[0].instance.pairing.division == 'Disney':
                    random_choice = string.ascii_uppercase[:8][:actual_round_num]
                else:
                    random_choice = string.ascii_uppercase[8:2 * 8][:actual_round_num]
                for round in Pairing.objects.get(pk=div1_pairing.pk).rounds.all():
                    if round.courtroom != None:
                        random_choice = random_choice.replace(round.courtroom, '')
                random_choice = random.sample(list(random_choice), len(random_choice))
                for form in div1_formset:
                    if form.instance.p_team != None and form.instance.d_team != None \
                            and form.instance.courtroom == None:
                        form.instance.courtroom = random_choice[0]
                        del(random_choice[0])
                        form.save()
                div1_formset.save()
            else:
                both_true = False

            if div2_formset.is_valid():
                actual_round_num = len(div2_formset)
                for form in div2_formset:
                    if form.instance.p_team == None or form.instance.d_team == None:
                        actual_round_num -= 1
                if div2_formset[0].instance.pairing.division == 'Disney':
                    random_choice = string.ascii_uppercase[:8][:actual_round_num]
                else:
                    random_choice = string.ascii_uppercase[8:2 * 8][:actual_round_num]
                for round in Pairing.objects.get(pk=div2_pairing.pk).rounds.all():
                    if round.courtroom != None:
                        random_choice = random_choice.replace(round.courtroom, '')
                random_choice = random.sample(list(random_choice), len(random_choice))
                for form in div2_formset:
                    if form.instance.p_team != None and form.instance.d_team != None \
                            and form.instance.courtroom == None:
                        form.instance.courtroom = random_choice[0]
                        del(random_choice[0])
                        form.save()
                div2_formset.save()
            else:
                both_true = False

            pairings = [div1_pairing, div2_pairing]
            for pairing in pairings:
                if pairing.final_submit and not pairing.publish:
                    for round in pairing.rounds.all():
                        if not Ballot.objects.filter(round=round).exists():
                            for judge in round.judges:
                                Ballot.objects.create(round=round, judge=judge)
                        else:
                            for judge in round.judges:
                                if not Ballot.objects.filter(round=round, judge=judge).exists():
                                    Ballot.objects.create(round=round, judge=judge)
                            for ballot in Ballot.objects.filter(round=round).all():
                                if ballot.judge not in round.judges:
                                    Ballot.objects.filter(round=round, judge=ballot.judge).delete()

            if both_true:
                return redirect('tourney:pairing_index')
        else:
            div1_formset = RoundFormSet(instance=div1_pairing,prefix='div1',
                                        form_kwargs={'pairing': div1_pairing,
                                                     'other_formset':None,
                                                     'request':request })
            div2_formset = RoundFormSet(instance=div2_pairing,prefix='div2',
                                        form_kwargs={'pairing': div2_pairing,
                                                     'other_formset':div1_formset,
                                                     'request':request })
            div1_submit_form = PairingSubmitForm(instance=div1_pairing, prefix='div1')
            div2_submit_form = PairingSubmitForm(instance=div2_pairing, prefix='div2')

        return render(request, 'tourney/pairing/edit.html', {'formsets': [div1_formset, div2_formset],
                                                             'submit_forms': [div1_submit_form, div2_submit_form],
                                                             'pairing': div1_pairing,
                                                             'judges': judges})
    else:
        if not Pairing.objects.filter(tournament=tournament, round_num=round_num).exists():
            pairing = Pairing.objects.create(tournament=tournament, round_num=round_num)
        else:
            pairing = Pairing.objects.get(tournament=tournament, round_num=round_num)

        available_judges_pk = [judge.pk for judge in Judge.objects.filter(user__tournament=tournament)
                               if judge.get_availability(pairing.round_num)]
        judges = Judge.objects.filter(pk__in=available_judges_pk).order_by('-checkin','-preside', 'user__username').all()

        if request.method == "POST":
            formset = RoundFormSet(request.POST, request.FILES, prefix='div1', instance=pairing,
                                        form_kwargs={'pairing': pairing,
                                                     'other_formset': None,
                                                     'request': request })
            submit_form = PairingSubmitForm(request.POST, prefix='div1', instance=pairing)

            if submit_form.is_valid():
                submit_form.save()

            both_true = True
            if formset.is_valid():
                # get courtroom
                actual_round_num = len(formset)
                for form in formset:
                    if form.instance.p_team == None or form.instance.d_team == None:
                        actual_round_num -= 1

                random_choice = string.ascii_uppercase[:int(tournament.division_team_num/2)][:actual_round_num]

                for round in Pairing.objects.get(pk=pairing.pk).rounds.all():
                    if round.courtroom != None:
                        random_choice = random_choice.replace(round.courtroom, '')
                random_choice = random.sample(list(random_choice), len(random_choice))
                for form in formset:
                    if form.instance.p_team != None and form.instance.d_team != None \
                            and form.instance.courtroom == None:
                        form.instance.courtroom = random_choice[0]
                        del (random_choice[0])
                        form.save()
                formset.save()
            else:
                both_true = False

            if both_true:
                pairings = [pairing]
                for pairing in pairings:
                    if pairing.final_submit and not pairing.publish:
                        for round in pairing.rounds.all():
                            if not Ballot.objects.filter(round=round).exists():
                                for judge in round.judges:
                                    Ballot.objects.create(round=round, judge=judge)
                            else:
                                for judge in round.judges:
                                    if not Ballot.objects.filter(round=round, judge=judge).exists():
                                        Ballot.objects.create(round=round, judge=judge)
                                for ballot in Ballot.objects.filter(round=round).all():
                                    if ballot.judge not in round.judges:
                                        Ballot.objects.filter(round=round, judge=ballot.judge).delete()
                return redirect('tourney:pairing_index')
        else:
            formset = RoundFormSet(instance=pairing, prefix='div1',
                                        form_kwargs={'pairing': pairing,
                                                     'other_formset': None,
                                                     'request': request})
            submit_form = PairingSubmitForm(instance=pairing, prefix='div1')

        return render(request, 'tourney/pairing/edit.html', {'formsets': [formset],
                                                             'submit_forms': [submit_form],
                                                             'pairing': pairing,
                                                             'judges': judges})

@user_passes_test(lambda u: u.is_staff)
def delete_pairing(request, round_num):
    if Pairing.objects.filter(tournament=request.user.tournament, round_num=round_num).exists():
        Pairing.objects.filter(tournament=request.user.tournament, round_num=round_num).delete()
    return redirect('tourney:pairing_index')

@login_required
def view_pairing(request, pk):
    pairing = Pairing.objects.get(pk=pk)
    if not pairing.team_submit:
        context = {}
    else:
        context = {'pairing': [pairing]}
    return render(request, 'tourney/pairing/view.html', context)

@user_passes_test(lambda u: u.is_staff)
def checkin_judges(request, round_num):

    if request.method == "POST":
        form = CheckinJudgeForm(request.POST, round_num=round_num, request=request)
        if form.is_valid():
            for judge in form.cleaned_data['checkins']:
                judge.checkin = True
                judge.save()
        return redirect('tourney:pairing_index')
    else:
        form = CheckinJudgeForm(round_num=round_num, request=request)

    return render(request, 'tourney/tab/checkin_judges.html',{'form':form, 'round_num':round_num})

@user_passes_test(lambda u: u.is_staff)
def clear_checkin(request):
    Judge.objects.update(checkin=False)
    return redirect('tourney:pairing_index')

@user_passes_test(lambda u: u.is_staff)
def checkin_all_judges(request, round_num):
    available_judges_pk = [judge.pk for judge in Judge.objects.filter(user__tournament=request.user.tournament)
                           if judge.get_availability(round_num)]
    Judge.objects.filter(pk__in=available_judges_pk).update(checkin=True)
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

@user_passes_test(lambda u: u.is_staff)
def view_captains_meeting_status(request, pairing_id):
    pairing = Pairing.objects.get(pk=pairing_id)
    captains_meetings = []
    for round in pairing.rounds.all():
        captains_meetings.append(round.captains_meeting)
    captains_meetings = sorted(captains_meetings, key=lambda x: x.round.courtroom)
    return render(request, 'tourney/tab/view_captains_meeting_status.html',
                  {'captains_meetings': captains_meetings})

# @login_required
# # def add_conflict(request):
# #     if request.method == 'POST':
# #         form = AddConflictForm(data=request.POST)
# #         if form.is_valid():
# #
# #     return render(request, 'tourney/add_conflict.html', {'form':form})

class ConflictUpdateView(JudgeOnlyMixin, PassRequestToFormViewMixin, UpdateView):
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

class JudgeFriendUpdateView(JudgeOnlyMixin, PassRequestToFormViewMixin, UpdateView):
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

@user_passes_test(lambda u: u.is_team)
def edit_competitor_pronouns(request):
    team = request.user.team
    if request.method == 'POST':
        competitor_pronouns_forms = [CompetitorPronounsForm(request.POST, instance=competitor,
                                                           prefix=competitor.name)
                                     for competitor in team.competitors.all()]
        for form in competitor_pronouns_forms:
            if form.is_valid():
                form.save()

        return redirect('index')
    else:
        competitor_pronouns_forms = [CompetitorPronounsForm(instance=competitor,
                                                           prefix=competitor.name)
                                     for competitor in team.competitors.all()]
    return render(request, 'tourney/competitor_pronouns.html', {
        'team': team,
        'forms': competitor_pronouns_forms
    })

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
            if pk == None:
                continue

            team_name = worksheet.cell(i, 2).value
            if Team.objects.filter(user__tournament=request.user.tournament, team_name=team_name).exists():
                pk = Team.objects.get(user__tournament=request.user.tournament, team_name=team_name).pk
            else:
                pk = None
            if worksheet.cell(i, 3).value != None or worksheet.cell(i, 3).value != '':
                division = worksheet.cell(i, 3).value
            else:
                division = None
            school = worksheet.cell(i, 4).value
            j = 5
            team_roster = []
            while j <= m and worksheet.cell(i,j).value != None and worksheet.cell(i,j).value != '':
                team_roster.append(worksheet.cell(i,j).value)
                j+=1
            message = ''
            # if len(team_roster) < 6:
            #     message += f' errors: team {pk} less than 6 members '
            # elif len(team_roster) > 10:
            #     message += f' errors: team {pk} more than 10 members '
            # else:

            try:
                if Team.objects.filter(pk=pk).exists():
                    Team.objects.filter(pk=pk).update(team_name=team_name,division=division,school=school)
                    team = Team.objects.get(pk=pk)
                    message += f' update team {team.pk} '
                else:
                    raw_password = worksheet.cell(i,17).value
                    username = ''.join(team_name.split(' '))
                    user = User(username=username, raw_password=raw_password, is_team=True, is_judge=False,
                                tournament=request.user.tournament)
                    user.set_password(raw_password)
                    user.tournament = request.user.tournament
                    user.save()
                    team = Team.objects.create(user=user, team_name=team_name,division=division,school=school)
                    message += f' create team {team.pk} '

                for name in team_roster:
                    if Competitor.objects.filter(team=team, name=name).exists():
                        message += f' update member {name} '
                        Competitor.objects.filter(team=team, name=name).update(team=team,name=name)
                    else:
                        message += f' create member {name} '
                        Competitor.objects.create(name=name,team=team)
            except Exception as e:
                message += str(e)
            else:
                message += ' success '
            list.append(message)
        return render(request, 'admin/load_excel.html', {"list": list})



@user_passes_test(lambda u: u.is_staff)
def load_judges(request):
    if "GET" == request.method:
        return render(request, 'admin/load_excel.html', {})
    else:
        excel_file = request.FILES["excel_file"]
        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Judges"]
        list = []
        n = worksheet.max_row
        m = worksheet.max_column
        for i in range(2, n + 1):
            username = worksheet.cell(i, 9).value
            if username == None or username == '':
                continue
            first_name = worksheet.cell(i, 1).value
            last_name = worksheet.cell(i, 2).value
            if last_name == None or last_name == '':
                last_name = ' '
            raw_password = worksheet.cell(i,10).value
            preside = worksheet.cell(i,3).value
            if preside == 'CIN' or 'No preference':
                preside = 2
            elif preside == 'y' or 'Presiding':
                preside = 1
            else:
                preside = 0
            availability = []
            for j in range(4, 9):
                if worksheet.cell(i, j).value == 'y' or worksheet.cell(i, j).value == 'YES':
                    availability.append(True)
                else:
                    availability.append(False)

            # judge_friends = worksheet.cell(i, 11).value
            # if judge_friends != None:
            #     judge_friends = judge_friends.split(',')

            message = ''
            try:
                if Judge.objects.filter(user__username=username).exists():
                    message += f'update judge {username}'
                    judge = Judge.objects.get(user__username=username)
                    user = judge.user
                    user.first_name = first_name
                    user.last_name = last_name
                    user.tournament = request.user.tournament
                    user.save()

                    # if judge_friends:
                    #     for friend in judge_friends:
                    #         first = friend.split(' ')[0]
                    #         last = friend.split(' ')[1]
                    #         if Judge.objects.filter(user__first_name=first, user__last_name=last).exists():
                    #             judge.judge_friends.add(Judge.objects.get(user__first_name=first, user__last_name=last))

                    judge.preside = preside
                    for i in range(len(availability)):
                        setattr(judge, f'available_round{i+1}', availability[i])
                    judge.save()
                else:
                    message += f'create judge {username}'
                    user = User(username=username,
                                first_name=first_name, last_name=last_name,
                                is_team=False, is_judge=True, tournament=request.user.tournament)
                    user.set_password(raw_password)
                    user.save()
                    judge = Judge(user=user, preside=preside)
                    for i in range(len(availability)):
                        setattr(judge, f'available_round{i+1}', availability[i])

                    # if judge_friends:
                    #     for friend in judge_friends:
                    #         first = friend.split(' ')[0]
                    #         last = friend.split(' ')[1]
                    #         if Judge.objects.filter(user__first_name=first, user__last_name=last).exists():
                    #             judge.judge_friends.add(Judge.objects.get(user__first_name=first, user__last_name=last))
                    judge.save()

            except Exception as e:
                message += str(e)
            else:
                message += ' success '
            list.append(message)
        return render(request, 'admin/load_excel.html', {"list": list})

@user_passes_test(lambda u: u.is_staff)
def load_sections(request):
    tournament = request.user.tournament
    if not Section.objects.filter(tournament=tournament).exists():
        wit_nums = tournament.wit_nums
        i = 1
        openings = Section.objects.create(name='Openings', tournament=tournament)
        SubSection.objects.create(name=f'{tournament.p_choice} Opening',
                                  section=openings,
                                  side='P',
                                  role='att',
                                  type='statement',
                                  help_text=f'{tournament.p_choice} Opening',
                                  sequence=i)
        SubSection.objects.create(name=f'Defense Opening',
                                  section=openings,
                                  side='D',
                                  role='att',
                                  type='statement',
                                  help_text=f'Defense Opening',
                                  sequence=i)
        i+=1
        side_choices = {
            'P': tournament.p_choice,
            'D': 'Defense'
        }
        for side in ['P', 'D']:
            for wit_num in range(1, wit_nums+1):

                section = Section.objects.create(name=f'{side_choices[side]} Witness #{wit_num}', tournament=tournament)
                SubSection.objects.create(name=f'{side} Wit {wit_num} Wit Direct',
                                          section=section,
                                          side=side,
                                          role='wit',
                                          type='direct',
                                          help_text=f'Witness (Direct)',
                                          sequence=i)
                SubSection.objects.create(name=f'{side} Wit {wit_num} Att Direct',
                                          section=section,
                                          side=side,
                                          role='att',
                                          type='direct',
                                          help_text=f'Directing Attorney',
                                          sequence=i)
                i+=1
                SubSection.objects.create(name=f'{side} Wit {wit_num} Wit Cross',
                                          section=section,
                                          side=side,
                                          role='wit',
                                          type='cross',
                                          help_text=f'Witness (Cross)',
                                          sequence=i)
                opposing_side = 'P' if side == 'D' else 'D'
                SubSection.objects.create(name=f'{side} Wit {wit_num} Att Cross',
                                          section=section,
                                          side=opposing_side,
                                          role='att',
                                          type='cross',
                                          help_text=f'Crossing Attorney',
                                          sequence=i)
                i+=1
        closings = Section.objects.create(name='Closings', tournament=tournament)
        SubSection.objects.create(name=f'{tournament.p_choice} Closing',
                                  section=closings,
                                  side='P',
                                  role='att',
                                  type='statement',
                                  help_text=f'{tournament.p_choice} Closing',
                                  sequence=i)
        SubSection.objects.create(name=f'Defense Closing',
                                  section=closings,
                                  side='D',
                                  role='att',
                                  type='statement',
                                  help_text=f'{tournament.p_choice} Closing',
                                  sequence=i)
    return redirect('index')