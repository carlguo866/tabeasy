from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
import django.contrib.auth.views as auth_views
from django.urls import reverse_lazy

from accounts.forms import *
from tourney.forms import JudgeForm, TeamForm
from tourney.models import Judge, Team, Competitor


def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(data=request.POST)
        judge_form = JudgeForm(data=request.POST)
        if user_form.is_valid() and judge_form.is_valid():

            user = user_form.save()
            setattr(user, f'is_judge', True)
            user.save()

            judge = judge_form.save(commit=False)
            judge.user = user
            judge.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = SignUpForm()
        judge_form = JudgeForm()

    context = {'forms': [user_form, judge_form]}
    return render(request, 'accounts/signup.html', context)


@user_passes_test(lambda u: u.is_staff)
def team_signup(request):
    tournament = request.user.tournament
    FormSet = inlineformset_factory(Team, Competitor,fields=('name', 'pronouns'),
                                         max_num=12, validate_max=True,
                                         extra=6)

    if request.method == 'POST':
        user_form = SignUpForm(data=request.POST, team_signup=True)
        team_form = TeamForm(data=request.POST)
        if user_form.is_valid() and team_form.is_valid():
            user = user_form.save()
            setattr(user, f'is_team', True)
            setattr(user, f'is_judge', False)
            user.save()

            team = team_form.save(commit=False)
            team.user = user
            team.save()
            formset = FormSet(request.POST, request.FILES, instance=team)
            if formset.is_valid():
                formset.save()
                return redirect('tourney:view_teams')
    else:
        user_form = SignUpForm(team_signup=True)
        formset = FormSet()
        team_form = TeamForm()

    context = {'user_form': user_form, 'formset': formset, 'team_form': team_form}
    return render(request, 'accounts/team_signup.html', context)

@user_passes_test(lambda u: u.is_staff)
def judge_signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(data=request.POST)
        judge_form = JudgeForm(data=request.POST)
        if user_form.is_valid() and judge_form.is_valid():

            user = user_form.save()
            setattr(user, f'is_judge', True)
            user.save()

            judge = judge_form.save(commit=False)
            judge.user = user
            judge.save()
            return redirect('tourney:view_judges')
    else:
        user_form = SignUpForm()
        judge_form = JudgeForm()

    context = {'forms': [user_form, judge_form]}
    return render(request, 'accounts/judge_signup.html', context)



class Login(auth_views.LoginView):
    template_name = 'accounts/login.html'

class Logout(auth_views.LogoutView):
    next_page = 'index'

class ChangePassword(auth_views.PasswordChangeView):
    template_name = 'accounts/change_password.html'

    success_url = reverse_lazy('accounts:password_change_done')

class DoneChangePassword(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/done_change_password.html'
