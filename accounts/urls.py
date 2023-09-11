from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('judge_signup/', views.judge_signup, name='judge_signup'),
    path('team_signup/', views.team_signup, name='team_signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('tournament/switch', views.UserTournamentView.as_view(), name='edit_tournament'),
    path('tournament/create', views.create_tournament, name='create_tournament'),
    path('change_password/', views.ChangePassword.as_view(),
         name='change_password'),
    path('password_change_done/', views.DoneChangePassword.as_view(),
         name='password_change_done'),
]