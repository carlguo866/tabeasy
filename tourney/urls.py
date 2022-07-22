from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'tourney'
urlpatterns = [
    path('pairing/', views.pairing, name='pairing'),
    path('judge/update_conflict',
         views.ConflictUpdateView.as_view(),
         name='update_conflict'),
    path('judge/submit_ballot',
         views.BallotCreateView.as_view(),
         name='submit_ballot'),
]