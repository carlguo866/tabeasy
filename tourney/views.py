import openpyxl
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.models import User
from tabeasy.utils.mixins import JudgeOnlyMixin
from tourney.forms import RoundForm, UpdateConflictForm, BallotForm, UpdateJudgeFriendForm, PairingFormSet, PairingForm, \
    CaptainsMeetingForm
from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Round, Pairing, CaptainsMeeting
from tourney.models.team import Team, TeamMember


def index(request):
    return render(request, 'index.html')

@user_passes_test(lambda u: u.is_staff)
def pairing_index(request):
    current_pairings = Pairing.objects.all()
    dict = {'pairings': current_pairings}
    return render(request, 'tourney/pairing/main.html', dict)


@user_passes_test(lambda u: u.is_staff)
def edit_pairing(request, pairing_id):
    RoundFormSet = inlineformset_factory(Pairing, Round, form=RoundForm, formset=PairingFormSet)
                                            # max_num=8, validate_max=True,
                                            # min_num=8, validate_min=True)
    if Pairing.objects.filter(pk=pairing_id).exists():
        pairing = Pairing.objects.get(pk=pairing_id)
        if request.method == "POST":
            formset = RoundFormSet(request.POST, request.FILES, instance=pairing, form_kwargs={'pairing': pairing})
            if formset.is_valid():
                formset.save()
                return redirect('tourney:pairing_index')
        else:
            formset = RoundFormSet(instance=pairing, form_kwargs={'pairing': pairing})
        return render(request, 'tourney/pairing/edit.html', {'formset': formset})
    else:
        if request.method == 'POST':
            pairing_form = PairingForm(request.POST, prefix='pairing')
            if pairing_form.is_valid():
                pairing = pairing_form.save()
                return redirect('tourney:pairing_index')
        else:
            pairing_form = PairingForm(prefix='pairing')
            return render(request, 'tourney/pairing/edit.html', {
                    'pairing_form': pairing_form,
                })






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

class BallotUpdateView(JudgeOnlyMixin, UpdateView):
    model = Ballot
    template_name = "tourney/ballot.html"
    form_class = BallotForm

    def get_success_url(self):
        return reverse_lazy('index') #

class CaptainsMeetingUpdateView(UpdateView):
    model = CaptainsMeeting
    template_name = "tourney/captains_meeting.html"
    form_class = CaptainsMeetingForm

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
                        raw_password = User.objects.make_random_password()
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

