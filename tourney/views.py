import math
import string
import random
from audioop import reverse
from functools import partial
import pinyin
import openpyxl
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms import inlineformset_factory, modelformset_factory
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.models import User
from tabeasy.utils.mixins import JudgeOnlyMixin
from tourney.forms import RoundForm, UpdateConflictForm, BallotForm, UpdateJudgeFriendForm, PairingFormSet
from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.round import Round, Pairing
from tourney.models.team import Team, TeamMember


def index(request):
    return render(request, 'index.html')

# @user_passes_test(lambda u: u.is_staff)
# def pairing(request):
#     div_1_teams = Team.objects.filter(division='Universal')
#     div_2_teams = Team.objects.filter(division='Disney')
#     dict = {'div_1_teams': div_1_teams, 'div_2_teams':div_2_teams,
#             'half_div_1_teams_num': math.ceil(float(len(div_1_teams))/2),
#             'half_div_2_teams_num': math.ceil(float(len(div_2_teams))/2),
#             'form': RoundForm()}
#     return render(request, 'tourney/pairing.html', dict)


@user_passes_test(lambda u: u.is_staff)
def create_pairing(request, pairing_id):
    pairing = Pairing.objects.get(pk=pairing_id)
    if pairing == None:
        pairing = Pairing(pk=pairing_id, division='Disney', round=1)
    RoundFormSet = inlineformset_factory(Pairing, Round, form=RoundForm, formset=PairingFormSet)
                                        # max_num=8, validate_max=True,
                                        # min_num=8, validate_min=True)
    if request.method == "POST":
        formset = RoundFormSet(request.POST, request.FILES, instance=pairing, form_kwargs={'pairing': pairing})
        if formset.is_valid():
            formset.save()
            return render(request, 'index.html')
    else:
        formset = RoundFormSet(instance=pairing, form_kwargs={'pairing': pairing})
    return render(request, 'tourney/pairing.html', {'formset': formset})

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
                        user = User(username=team_name, raw_password=raw_password, is_team=True)
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

