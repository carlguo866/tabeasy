from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'tourney'
urlpatterns = [
    path('captains_meeting/<int:pk>',
         views.CaptainsMeetingUpdateView.as_view(),
         name='captains_meeting'),
    path('pairing', views.pairing_index, name='pairing_index'),
    path('pairing/edit/<int:round_num>', views.edit_pairing, name='edit_pairing'),
    path('pairing/delete/<int:round_num>', views.delete_pairing, name='delete_pairing'),
    path('pairing/next_pairing', views.next_pairing, name='next_pairing'),
    path('checkin_judges/<int:round_num>', views.checkin_judges, name='checkin_judges'),
    path('clear_checkin/', views.clear_checkin, name='clear_checkin'),
    path('checkin_all_judges/<int:round_num>', views.checkin_all_judges, name='checkin_all_judges'),
    path('view_ballot_status/<int:pairing_id>', views.view_ballot_status, name='view_ballot_status'),
    path('results', views.results, name='results'),
    path('individual_awards', views.individual_awards, name='individual_awards'),
    path('judge/update_conflict',
         views.ConflictUpdateView.as_view(),
         name='update_conflict'),
    path('judge/judge_friends',
         views.JudgeFriendUpdateView.as_view(),
         name='judge_friend'),
    path('judge/judge_preference',
         views.JudgePreferenceUpdateView.as_view(),
         name='edit_preference'),
    path('ballot/<int:pk>',
         views.BallotUpdateView.as_view(),
         name='submit_ballot'),
]
