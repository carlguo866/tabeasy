from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
import django.contrib.auth.views as auth_views
from accounts.forms import *
from tourney.forms import JudgeForm, TeamForm


def single_true(iterable):
    i = iter(iterable)
    return any(i) and not any(i)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()  # why? this seems to create the user
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            user.raw_password = raw_password
            user.is_judge = form.cleaned_data.get('is_judge')
            user.is_team = form.cleaned_data.get('is_team')
            user.is_tab = form.cleaned_data.get('is_tab')
            if not single_true([user.is_judge,user.is_team, user.is_tab]):
                raise Http404("ur both a team and a judge")
            user.save()

            if user.is_judge:
                print('is_judge')
                role_form = JudgeForm(data=request.POST)
            elif user.is_team:
                print('is_team')
                role_form = TeamForm(data=request.POST)
            else:
                print('is_tab')
                role_form = TabForm(data=request.POST)
            role = role_form.save(commit=False)
            role.user = user
            role.save()

            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

class Login(auth_views.LoginView):
    template_name = 'accounts/login.html'

class Logout(auth_views.LogoutView):
    next_page = 'index'