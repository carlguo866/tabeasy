from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
import django.contrib.auth.views as auth_views
from accounts.forms import *
from tourney.forms import JudgeForm, TeamForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password=raw_password)
            if form.cleaned_data.get('is_team'):
                user.raw_password = raw_password
            user.save()

            if user.is_judge:
                role_form = JudgeForm(data=request.POST)
            elif user.is_team:
                role_form = TeamForm(data=request.POST)
            role = role_form.save(commit=False)
            role.user = user
            role.preside = form.cleaned_data.get('preside')
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