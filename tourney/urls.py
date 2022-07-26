from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'tourney'
urlpatterns = [
    path('pairing', views.pairing_index, name='pairing_index'),
    path('pairing/<int:pairing_id>', views.edit_pairing, name='edit_pairing'),
    path('judge/update_conflict',
         views.ConflictUpdateView.as_view(),
         name='update_conflict'),
    path('judge/judge_friends',
         views.JudgeFriendUpdateView.as_view(),
         name='judge_friend'),
    path('judge/submit_ballot/<int:pk>',
         views.BallotUpdateView.as_view(),
         name='submit_ballot'),
]