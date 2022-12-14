from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'tourney'
urlpatterns = [

    path('refresh', views.refresh, name='refresh'),
    path('pairing', views.pairing_index, name='pairing_index'),
    path('pairing/<int:pk>', views.view_pairing, name='view_pairing'),
    path('pairing/edit/<int:round_num>', views.edit_pairing, name='edit_pairing'),
    path('pairing/delete/<int:round_num>', views.delete_pairing, name='delete_pairing'),
    path('pairing/next_pairing/<int:round_num>', views.next_pairing, name='next_pairing'),
    path('checkin_judges/<int:round_num>', views.checkin_judges, name='checkin_judges'),
    path('clear_checkin/', views.clear_checkin, name='clear_checkin'),
    path('checkin_all_judges/<int:round_num>', views.checkin_all_judges, name='checkin_all_judges'),
    path('view_ballot_status/<int:pairing_id>', views.view_ballot_status, name='view_ballot_status'),
    path('tournament_setting', views.TournamentUpdateView.as_view(),  name='tournament_setting'),
    path('team', views.view_teams, name='view_teams'),
    path('team/<int:pk>', views.view_individual_team, name='view_individual_team'),
    path('team/delete/<int:pk>', views.delete_individual_team, name='delete_individual_team'),
    path('captains_meeting/<int:pairing_id>',
         views.view_captains_meeting_status, name='view_captains_meeting_status'),
    path('results', views.results, name='results'),
    path('individual_awards', views.individual_awards, name='individual_awards'),
    path('team/edit_competitor_pronouns/',
         views.edit_competitor_pronouns,
         name='edit_competitor_pronouns'),
    path('judge', views.view_judges, name='view_judges'),
    path('judge/delete/<int:pk>', views.delete_individual_judge, name='delete_individual_judge'),
    path('judge/<int:pk>', views.view_individual_judge, name='view_individual_judge'),
    path('judge/update_conflict',
         views.ConflictUpdateView.as_view(),
         name='update_conflict'),
    path('judge/judge_friends',
         views.JudgeFriendUpdateView.as_view(),
         name='judge_friend'),
    path('judge/judge_preference',
         views.JudgePreferenceUpdateView.as_view(),
         name='edit_preference'),

]
