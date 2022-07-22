import math
import string
import random
from audioop import reverse

import pinyin
import openpyxl
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.models import User
from tabeasy.utils.mixins import JudgeOnlyMixin
from tourney.forms import PairingFormSimple, RoundForm, UpdateConflictForm
from tourney.models.ballot import Ballot
from tourney.models.judge import Judge
from tourney.models.team import Team


def index(request):
    return render(request, 'index.html')

@user_passes_test(lambda u: u.is_staff)
def pairing(request):
    div_1_teams = Team.objects.filter(division='Universal')
    div_2_teams = Team.objects.filter(division='Disney')
    dict = {'div_1_teams': div_1_teams, 'div_2_teams':div_2_teams,
            'half_div_1_teams_num': math.ceil(float(len(div_1_teams))/2),
            'half_div_2_teams_num': math.ceil(float(len(div_2_teams))/2),
            'form': RoundForm()}
    return render(request, 'tourney/pairing.html', dict)


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
    # fields = ['conflicts']
    #
    # def form_valid(self, form):
    #     form.instance.judge = self.request.user.judge
    #     return super().form_valid(form)
    # #
    form_class = UpdateConflictForm
    def get_object(self, queryset=None):
        return self.request.user.judge

    success_url = reverse_lazy('index')

class BallotCreateView(CreateView):
    model = Ballot
    template_name = "tourney/add_conflict.html"

    fields = ['courtroom', 'p_team','d_team','judge','round_num',
              'p_open','p_open_comment','d_open','d_open_comment']

    # def form_valid(self, form):
    #
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('index', args=[self.object.pk])


def generate_random_password():
    chars = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    return "".join(random.choice(chars) for _ in range(8))

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
                        Team.objects.filter(pk=pk).update(team_name=team_name,division=division,school=school, team_roster=team_roster)
                    else:
                        message += f'create team {pk}'
                        raw_password = User.objects.make_random_password()
                        user = User(username=team_name, raw_password=raw_password, is_team=True)
                        user.set_password(raw_password)
                        user.save()
                        Team.objects.create(team_id=pk, user=user, team_name=team_name,division=division,school=school, team_roster=team_roster)
                except Exception as e:
                    message += str(e)
                else:
                    message += 'success'
            list.append(message)
        return render(request, 'admin/load_excel.html', {"list": list})

