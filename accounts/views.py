from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
import django.contrib.auth.views as auth_views
from accounts.forms import *
from tourney.forms import JudgeForm, TeamForm

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
            for round in judge_form.cleaned_data['availability']:
                setattr(judge, round, True)
            judge.save()
            login(request, user)
            return redirect('index')
    else:
        user_form = SignUpForm()
        judge_form = JudgeForm()

    context = {'forms': [user_form, judge_form]}
    return render(request, 'accounts/signup.html', context)

class Login(auth_views.LoginView):
    template_name = 'accounts/login.html'

class Logout(auth_views.LogoutView):
    next_page = 'index'