from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'ballot'
urlpatterns = [
    path('ballot/<str:encrypted_pk>',
     views.BallotUpdateView.as_view(),
     name='view'),
    path('captains_meeting/<str:encrypted_pk>',
         views.CaptainsMeetingUpdateView.as_view(),
         name='captains_meeting'),
]