import random
import string
import openpyxl
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from accounts.models import User
from tabeasy.settings import DEBUG
from tabeasy.utils.mixins import JudgeOnlyMixin, PassRequestToFormViewMixin
from tabeasy_secrets.secret import DIVISION_ROUND_NUM, str_int, TOURNAMENT_NAME
from tourney.forms import RoundForm, UpdateConflictForm, UpdateJudgeFriendForm, PairingFormSet, \
    CaptainsMeetingForm, PairingSubmitForm, JudgeForm, CheckinJudgeForm, EditPronounsForm
from submission.models.ballot import Ballot
from tourney.models.captains_meeting import Character, CharacterPronouns
from tourney.models.judge import Judge
from tourney.models.round import Round, Pairing, CaptainsMeeting
from tourney.models.team import Team
from tourney.models.competitor import Competitor

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
    atts_ranked = [(member,'P',member.att_individual_score()[0]) for member in Competitor.objects.all()
                   if member.att_individual_score()[0] >= 10]+ \
                  [(member, 'D', member.att_individual_score()[1]) for member in Competitor.objects.all()
                   if member.att_individual_score()[1] >= 10]
    atts_ranked = sorted(atts_ranked, key=lambda x: -x[2])
    wits_ranked = [(member,'P',member.wit_individual_score()[0]) for member in Competitor.objects.all()
                   if member.wit_individual_score()[0] >= 10]+ \
                  [(member, 'D', member.wit_individual_score()[1]) for member in Competitor.objects.all()
                   if member.wit_individual_score()[1] >= 10]
    wits_ranked = sorted(wits_ranked, key=lambda x: -x[2])

    dict = {'ranked': zip(atts_ranked,wits_ranked)}
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
                                    form_kwargs={'pairing': div1_pairing, 'other_formset':None})
        div2_formset = RoundFormSet(request.POST, request.FILES, prefix='div2', instance=div2_pairing,
                                    form_kwargs={'pairing': div2_pairing, 'other_formset':div1_formset})

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
                random_choice = string.ascii_uppercase[:DIVISION_ROUND_NUM][:actual_round_num]
            else:
                random_choice = string.ascii_uppercase[DIVISION_ROUND_NUM:2 * DIVISION_ROUND_NUM][:actual_round_num]
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
                random_choice = string.ascii_uppercase[:DIVISION_ROUND_NUM][:actual_round_num]
            else:
                random_choice = string.ascii_uppercase[DIVISION_ROUND_NUM:2 * DIVISION_ROUND_NUM][:actual_round_num]
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
        div1_formset = RoundFormSet(instance=div1_pairing,prefix='div1', form_kwargs={'pairing': div1_pairing, 'other_formset':None})
        div2_formset = RoundFormSet(instance=div2_pairing,prefix='div2', form_kwargs={'pairing': div2_pairing, 'other_formset':div1_formset})
        div1_submit_form = PairingSubmitForm(instance=div1_pairing, prefix='div1')
        div2_submit_form = PairingSubmitForm(instance=div2_pairing, prefix='div2')
    return render(request, 'tourney/pairing/edit.html', {'formsets': [div1_formset, div2_formset],
                                                         'submit_forms': [div1_submit_form,div2_submit_form],
                                                         'pairing': div1_pairing,
                                                         'judges': judges})
@user_passes_test(lambda u: u.is_staff)
def delete_pairing(request, round_num):
    if Pairing.objects.filter(round_num=round_num).exists():
        Pairing.objects.filter(round_num=round_num).delete()
    return redirect('tourney:pairing_index')

@user_passes_test(lambda u: u.is_staff)
def checkin_judges(request, round_num):

    if request.method == "POST":
        form = CheckinJudgeForm(request.POST, round_num=round_num)
        if form.is_valid():
            for judge in form.cleaned_data['checkins']:
                judge.checkin = True
                judge.save()
        return redirect('tourney:pairing_index')
    else:
        form = CheckinJudgeForm(round_num=round_num)

    return render(request, 'tourney/tab/checkin_judges.html',{'form':form, 'round_num':round_num})

@user_passes_test(lambda u: u.is_staff)
def clear_checkin(request):
    Judge.objects.update(checkin=False)
    return redirect('tourney:pairing_index')

@user_passes_test(lambda u: u.is_staff)
def checkin_all_judges(request, round_num):
    available_judges_pk = [judge.pk for judge in Judge.objects.all()
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

@user_passes_test(lambda u: u.is_staff)
def test_pronouns(request):
    if request.method == "POST":
        forms = [EditPronounsForm(request.POST, instance=character,prefix=character.__str__())
                 for character in Character.objects.all()]
        has_wrong = False
        for form in forms:
            if form.is_valid():
               form.save()
            else:
                has_wrong = True
        if has_wrong:
            raise ValidationError('aldfnkalndln somethign wrong')
        else:
            return redirect('index')
    else:
        forms = [EditPronounsForm(instance=character,prefix=character.__str__())
                 for character in Character.objects.all()]

    context = {'forms': forms}
    return render(request, 'accounts/signup.html',
                  context)


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

class CaptainsMeetingUpdateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, UpdateView):
    model = CaptainsMeeting
    template_name = "tourney/captains_meeting.html"
    form_class = CaptainsMeetingForm
    permission_denied_message = 'You are not allowed to view this Captains Meeting Form.'

    def test_func(self):
        self.captains_meeting = get_object_or_404(CaptainsMeeting, pk=str_int(self.kwargs['encrypted_pk']))
        if self.request.user.is_staff:
            return True
        if self.request.user.is_team and self.request.user.team not in self.captains_meeting.round.teams:
            return False
        if self.request.user.is_judge and \
                self.request.user.judge not in self.captains_meeting.round.judges:
            return False
        return True

    def get_object(self, queryset=None):
        return CaptainsMeeting.objects.get(pk=str_int(self.kwargs['encrypted_pk']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if CharacterPronouns.objects.filter(captains_meeting=self.object).exists():
            context['forms'] = [EditPronounsForm(instance=character_pronouns,
                                                 character=character_pronouns.character,captains_meeting=self.object,
                                                 prefix=character_pronouns.character.__str__())
                                for character_pronouns in
                                CharacterPronouns.objects.filter(captains_meeting=self.object).all()]
        else:
            context['forms'] = [EditPronounsForm(character=character,captains_meeting=self.object,
                                                 prefix=character.__str__())
                 for character in Character.objects.filter(tournament__name=TOURNAMENT_NAME).all()]
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if CharacterPronouns.objects.filter(captains_meeting=self.object).exists():
            forms = [EditPronounsForm(request.POST, instance=character_pronouns,
                                                 character=character_pronouns.character,
                                                captains_meeting=self.object,
                                                 prefix=character_pronouns.character.__str__())
                                for character_pronouns in
                                CharacterPronouns.objects.filter(captains_meeting=self.object).all()]
        else:
            forms = [EditPronounsForm(request.POST, character=character,captains_meeting=self.object, prefix=character.__str__())
                       for character in Character.objects.all()]
        is_valid = True
        for pronouns_form in forms:
            if not pronouns_form.is_valid():
                raise ValidationError(pronouns_form.errors)
                is_valid = False
        if not form.is_valid():
            is_valid = False
        if is_valid:
            return self.form_valid(form, forms)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, forms):
        for pronouns_form in forms:
            # pronouns_form.instance.captains_meeting = self.object
            pronouns_form.save()
        return super().form_valid(form)

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
                        if Competitor.objects.filter(name=name).exists():
                            message += f'update member {name}'
                            Competitor.objects.filter(name=name).update(team=Team.objects.filter(pk=pk)[0],name=name)
                        else:
                            message += f'create member {name}'
                            Competitor.objects.create(name=name,team=Team.objects.filter(pk=pk)[0])
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
            if username == None or username == '':
                continue
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
            for j in range(4, 9):
                if worksheet.cell(i, j).value == 'y':
                    availability.append(True)
                else:
                    availability.append(False)

            judge_friends = worksheet.cell(i, 11).value
            if judge_friends != None:
                judge_friends = judge_friends.split(',')

            message = ''
            try:
                if Judge.objects.filter(user__username=username).exists():
                    message += f'update judge {username}'
                    judge = Judge.objects.get(user__username=username)
                    user = judge.user
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    if judge_friends:
                        for friend in judge_friends:
                            first = friend.split(' ')[0]
                            last = friend.split(' ')[1]
                            if Judge.objects.filter(user__first_name=first, user__last_name=last).exists():
                                judge.judge_friends.add(Judge.objects.get(user__first_name=first, user__last_name=last))

                    judge.preside = preside
                    for i in range(len(availability)):
                        setattr(judge, f'available_round{i+1}', availability[i])
                    judge.save()
                else:
                    message += f'create judge {username}'
                    user = User(username=username,
                                first_name=first_name, last_name=last_name,
                                is_team=False, is_judge=True)
                    user.set_password(raw_password)
                    user.save()
                    judge = Judge(user=user, preside=preside)
                    for i in range(len(availability)):
                        setattr(judge, f'available_round{i+1}', availability[i])

                    if judge_friends:
                        for friend in judge_friends:
                            first = friend.split(' ')[0]
                            last = friend.split(' ')[1]
                            if Judge.objects.filter(user__first_name=first, user__last_name=last).exists():
                                judge.judge_friends.add(Judge.objects.get(user__first_name=first, user__last_name=last))
                    judge.save()

            except Exception as e:
                message += str(e)
            else:
                message += 'success'
            list.append(message)
        return render(request, 'admin/load_excel.html', {"list": list})